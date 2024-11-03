from abc import ABC, abstractmethod
from typing import Any

class EventSubscriber(ABC):
    @abstractmethod
    def handle(self, event: Any) -> None:
        pass