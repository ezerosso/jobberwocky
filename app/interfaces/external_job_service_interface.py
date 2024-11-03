from abc import ABC, abstractmethod
from typing import Dict, List
class ExternalJobSourceInterface(ABC):
    @abstractmethod
    def fetch_jobs(self) -> List[Dict]:
        pass