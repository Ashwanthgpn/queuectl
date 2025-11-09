import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class JobState(Enum):
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD = "dead"

class Job:
    def __init__(
        self,
        command: str,
        job_id: Optional[str] = None,
        max_retries: int = 3,
        created_at: Optional[str] = None,
        **kwargs
    ):
        self.id = job_id or str(uuid.uuid4())
        self.command = command
        self.state = JobState.PENDING
        self.attempts = 0
        self.max_retries = max_retries
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        self.started_at = None
        self.finished_at = None
        self.last_error = None
        self.output = None
        self.backoff_base = kwargs.get('backoff_base', 2)
        self.timeout = kwargs.get('timeout', 30)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "command": self.command,
            "state": self.state.value,
            "attempts": self.attempts,
            "max_retries": self.max_retries,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "last_error": self.last_error,
            "output": self.output,
            "backoff_base": self.backoff_base,
            "timeout": self.timeout
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Job':
        job = cls(
            command=data['command'],
            job_id=data['id'],
            max_retries=data.get('max_retries', 3),
            created_at=data.get('created_at'),
            backoff_base=data.get('backoff_base', 2),
            timeout=data.get('timeout', 30)
        )
        job.state = JobState(data['state'])
        job.attempts = data.get('attempts', 0)
        job.updated_at = data.get('updated_at', job.created_at)
        job.started_at = data.get('started_at')
        job.finished_at = data.get('finished_at')
        job.last_error = data.get('last_error')
        job.output = data.get('output')
        return job

    def mark_processing(self):
        self.state = JobState.PROCESSING
        self.attempts += 1
        self.started_at = datetime.utcnow().isoformat()
        self.updated_at = self.started_at

    def mark_completed(self, output: str = None):
        self.state = JobState.COMPLETED
        self.finished_at = datetime.utcnow().isoformat()
        self.updated_at = self.finished_at
        self.output = output

    def mark_failed(self, error: str = None):
        self.state = JobState.FAILED
        self.finished_at = datetime.utcnow().isoformat()
        self.updated_at = self.finished_at
        self.last_error = error

    def mark_dead(self):
        self.state = JobState.DEAD
        self.finished_at = datetime.utcnow().isoformat()
        self.updated_at = self.finished_at

    def should_retry(self) -> bool:
        return (self.state == JobState.FAILED and 
                self.attempts <= self.max_retries)

    def get_retry_delay(self) -> float:
        return self.backoff_base ** self.attempts

    def is_expired(self) -> bool:
        return (self.state == JobState.FAILED and 
                self.attempts >= self.max_retries)