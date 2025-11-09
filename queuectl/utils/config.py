import json
from typing import Dict, Any

class Config:
    _defaults = {
        "max_retries": 3,
        "backoff_base": 2,
        "job_timeout": 30,
        "worker_count": 1,
        "storage_path": "queuectl_data",
        "log_level": "INFO"
    }
    
    def __init__(self, storage):
        self.storage = storage
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        stored_config = self.storage.load_config()
        config = self._defaults.copy()
        config.update(stored_config)
        return config

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        self._config[key] = value
        return self.storage.save_config(self._config)

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()

    def reset(self) -> bool:
        self._config = self._defaults.copy()
        return self.storage.save_config(self._config)