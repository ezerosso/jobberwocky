from dataclasses import dataclass
import os
from typing import Any, Dict

@dataclass
class CeleryConfig:
    broker_url: str
    result_backend: str
    beat_schedule: Dict[str, Any]
    
    @classmethod
    def default_config(cls) -> 'CeleryConfig':
        return cls(
            broker_url=os.getenv('CELERY_BROKER_URL'),
            result_backend=os.getenv('CELERY_RESULT_BACKEND'),
            beat_schedule={
                'log-every-5-minutes': {
                    'task': 'app.tasks.external_jobs_task.log_task',
                    'schedule': 300.0,
                }
            }
    )

@dataclass
class AppConfig:
    SQLALCHEMY_DATABASE_URI: str
    GITHUB_JOBS_URL: str
    CELERY: CeleryConfig
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        return cls(
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
            GITHUB_JOBS_URL=os.getenv('GITHUB_JOBS_URL'),
            CELERY=CeleryConfig.default_config()
        )
