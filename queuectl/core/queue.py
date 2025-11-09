import logging
import time
from typing import List, Optional, Dict, Any
from datetime import datetime
from .job import Job, JobState
from .storage import JobStorage

logger = logging.getLogger(__name__)

class JobQueue:
    def __init__(self, storage: JobStorage):
        self.storage = storage
        self._running = False

    def enqueue(self, command: str, **kwargs) -> Optional[Job]:
        try:
            job = Job(command, **kwargs)
            if self.storage.save_job(job):
                logger.info(f"Enqueued job {job.id}: {command}")
                return job
            return None
        except Exception as e:
            logger.error(f"Error enqueueing job: {e}")
            return None

    def get_next_pending_job(self, worker_id: str) -> Optional[Job]:
        pending_jobs = self.storage.get_jobs_by_state(JobState.PENDING)
        
        for job in pending_jobs:
            if self.storage.acquire_job_lock(job.id, worker_id):
                current_job = self.storage.get_job(job.id)
                if current_job and current_job.state == JobState.PENDING:
                    current_job.mark_processing()
                    if self.storage.save_job(current_job):
                        return current_job
                    else:
                        self.storage.release_job_lock(job.id)
                else:
                    self.storage.release_job_lock(job.id)
        
        return None

    def complete_job(self, job: Job, output: str = None) -> bool:
        job.mark_completed(output)
        success = self.storage.save_job(job)
        if success:
            self.storage.release_job_lock(job.id)
        return success

    def fail_job(self, job: Job, error: str = None) -> bool:
        job.mark_failed(error)
        
        if job.is_expired():
            job.mark_dead()
            logger.warning(f"Job {job.id} moved to DLQ after {job.attempts} attempts")
        
        success = self.storage.save_job(job)
        if success:
            self.storage.release_job_lock(job.id)
        return success

    def retry_dlq_job(self, job_id: str) -> bool:
        job = self.storage.get_job(job_id)
        if not job or job.state != JobState.DEAD:
            return False
        
        job.state = JobState.PENDING
        job.attempts = 0
        job.last_error = None
        job.started_at = None
        job.finished_at = None
        job.updated_at = datetime.utcnow().isoformat()
        
        return self.storage.save_job(job)

    def get_stats(self) -> Dict[str, Any]:
        all_jobs = self.storage.get_all_jobs()
        stats = {
            "total_jobs": len(all_jobs),
            "pending": 0,
            "processing": 0,
            "completed": 0,
            "failed": 0,
            "dead": 0
        }
        
        for job in all_jobs.values():
            stats[job.state.value] += 1
        
        return stats

    def cleanup_orphaned_locks(self, max_age: float = 3600) -> int:
        try:
            locks = self.storage.load_config().get('locks', {})
            current_time = time.time()
            orphaned_count = 0
            
            locks_to_remove = []
            for job_id, lock_info in locks.items():
                lock_age = current_time - lock_info.get('locked_at', 0)
                if lock_age > max_age:
                    locks_to_remove.append(job_id)
                    orphaned_count += 1
            
            for job_id in locks_to_remove:
                del locks[job_id]
            
            if locks_to_remove:
                config = self.storage.load_config()
                config['locks'] = locks
                self.storage.save_config(config)
            
            return orphaned_count
                
        except Exception as e:
            logger.error(f"Failed to cleanup orphaned locks: {e}")
            return 0