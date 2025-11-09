import json
import os
import time
from typing import Dict, List, Optional
from pathlib import Path
import logging
from .job import Job, JobState

logger = logging.getLogger(__name__)

class JobStorage:
    def __init__(self, storage_path: str = "queuectl_data"):
        self.storage_path = Path(storage_path)
        self.jobs_file = self.storage_path / "jobs.json"
        self.locks_file = self.storage_path / "locks.json"
        self.config_file = self.storage_path / "config.json"
        
        self._ensure_storage_dir()
        self._initialize_files()

    def _ensure_storage_dir(self):
        self.storage_path.mkdir(exist_ok=True)

    def _initialize_files(self):
        for file_path in [self.jobs_file, self.locks_file, self.config_file]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump({}, f)

    def _atomic_file_operation(self, file_path, operation):
        """Simple atomic file operation using file moves"""
        temp_file = file_path.with_suffix('.tmp')
        try:
            # Read current data
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            # Perform operation
            result = operation(data)
            
            # Write to temp file
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Atomic replace
            os.replace(temp_file, file_path)
            return result
            
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise e

    def save_job(self, job: Job) -> bool:
        try:
            def update_data(data):
                data[job.id] = job.to_dict()
                return True
            
            return self._atomic_file_operation(self.jobs_file, update_data)
        except Exception as e:
            logger.error(f"Failed to save job {job.id}: {e}")
            return False

    def get_job(self, job_id: str) -> Optional[Job]:
        try:
            def read_data(data):
                job_data = data.get(job_id)
                if job_data:
                    return Job.from_dict(job_data)
                return None
            
            return self._atomic_file_operation(self.jobs_file, read_data)
        except Exception as e:
            logger.error(f"Failed to get job {job.id}: {e}")
            return None

    def get_all_jobs(self) -> Dict[str, Job]:
        try:
            def read_data(data):
                return {job_id: Job.from_dict(job_data) for job_id, job_data in data.items()}
            
            return self._atomic_file_operation(self.jobs_file, read_data)
        except Exception as e:
            logger.error(f"Failed to get all jobs: {e}")
            return {}

    def get_jobs_by_state(self, state: JobState) -> List[Job]:
        all_jobs = self.get_all_jobs()
        return [job for job in all_jobs.values() if job.state == state]

    def delete_job(self, job_id: str) -> bool:
        try:
            def update_data(data):
                if job_id in data:
                    del data[job_id]
                    return True
                return False
            
            return self._atomic_file_operation(self.jobs_file, update_data)
        except Exception as e:
            logger.error(f"Failed to delete job {job_id}: {e}")
            return False

    def acquire_job_lock(self, job_id: str, worker_id: str) -> bool:
        try:
            def update_data(data):
                if job_id in data:
                    return False  # Already locked
                data[job_id] = {
                    "worker_id": worker_id,
                    "locked_at": time.time()
                }
                return True
            
            return self._atomic_file_operation(self.locks_file, update_data)
        except Exception as e:
            logger.error(f"Failed to acquire lock for job {job_id}: {e}")
            return False

    def release_job_lock(self, job_id: str) -> bool:
        try:
            def update_data(data):
                if job_id in data:
                    del data[job_id]
                    return True
                return False
            
            return self._atomic_file_operation(self.locks_file, update_data)
        except Exception as e:
            logger.error(f"Failed to release lock for job {job_id}: {e}")
            return False

    def save_config(self, config: Dict) -> bool:
        try:
            def update_data(data):
                data.clear()
                data.update(config)
                return True
            
            return self._atomic_file_operation(self.config_file, update_data)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def load_config(self) -> Dict:
        try:
            def read_data(data):
                return data.copy()
            
            return self._atomic_file_operation(self.config_file, read_data)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}