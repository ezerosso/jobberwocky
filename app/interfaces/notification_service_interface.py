from abc import ABC, abstractmethod

class NotificationServiceInterface(ABC):
    @abstractmethod
    def notify(self, dir: str, job_data: dict):
        pass