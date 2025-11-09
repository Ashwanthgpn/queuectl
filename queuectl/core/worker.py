import subprocess
import time
import logging
import signal
import sys
import threading
from typing import Optional, Dict
from datetime import datetime
from .job import Job
from .queue import JobQueue

logger = logging.getLogger(__name__)

class JobWorker:
    def __init__(self, worker_id: str, queue: JobQueue):
        self.worker_id = worker_id
        self.queue = queue
        self.running = False
        self.current_job: Optional[Job] = None
        self.processed_count = 0
        self.failed_count = 0
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info(f"Worker {self.worker_id} received shutdown signal")
        self.running = False

    def start(self):
        self.running = True
        logger.info(f"Worker {self.worker_id} started")
        
        while self.running:
            try:
                job = self.queue.get_next_pending_job(self.worker_id)
                
                if job:
                    self.current_job = job
                    self._process_job(job)
                    self.current_job = None
                else:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Worker {self.worker_id} error: {e}")
                time.sleep(5)
        
        logger.info(f"Worker {self.worker_id} stopped")

    def _process_job(self, job: Job):
        logger.info(f"Worker {self.worker_id} processing job {job.id}: {job.command}")
        
        try:
            start_time = time.time()
            result = subprocess.run(
                job.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=job.timeout
            )
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                self.queue.complete_job(job, result.stdout)
                self.processed_count += 1
                logger.info(f"Job {job.id} completed in {execution_time:.2f}s")
            else:
                error_msg = f"Exit code {result.returncode}: {result.stderr}"
                self.queue.fail_job(job, error_msg)
                self.failed_count += 1
                logger.warning(f"Job {job.id} failed: {error_msg}")
                
        except subprocess.TimeoutExpired:
            error_msg = f"Timeout after {job.timeout}s"
            self.queue.fail_job(job, error_msg)
            self.failed_count += 1
            logger.error(f"Job {job.id} timeout")
            
        except Exception as e:
            error_msg = f"System error: {str(e)}"
            self.queue.fail_job(job, error_msg)
            self.failed_count += 1
            logger.error(f"Job {job.id} system error: {error_msg}")

    def stop(self):
        self.running = False

    def get_stats(self) -> dict:
        return {
            "worker_id": self.worker_id,
            "processed": self.processed_count,
            "failed": self.failed_count,
            "current_job": self.current_job.id if self.current_job else None,
            "running": self.running
        }


class WorkerManager:
    def __init__(self, queue: JobQueue):
        self.queue = queue
        self.workers: Dict[str, JobWorker] = {}
        self.threads: Dict[str, threading.Thread] = {}

    def start_workers(self, count: int = 1):
        for i in range(count):
            worker_id = f"worker-{len(self.workers) + 1}"
            worker = JobWorker(worker_id, self.queue)
            self.workers[worker_id] = worker
            
            thread = threading.Thread(target=worker.start, daemon=True)
            thread.start()
            self.threads[worker_id] = thread
            
            logger.info(f"Started {worker_id}")

    def stop_workers(self):
        for worker_id, worker in self.workers.items():
            worker.stop()
            logger.info(f"Stopped {worker_id}")
        
        # Wait for threads to finish
        for thread in self.threads.values():
            thread.join(timeout=10)
        
        self.workers.clear()
        self.threads.clear()

    def get_worker_stats(self) -> List[dict]:
        return [worker.get_stats() for worker in self.workers.values()]