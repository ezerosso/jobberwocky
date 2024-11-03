from dataclasses import dataclass
import datetime
from typing import List

@dataclass
class JobCreatedEvent:
    id: str
    title: str
    company: str
    location: str
    skills: List[str]
    created_at: datetime