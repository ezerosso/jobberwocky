

from abc import abstractmethod
from typing import List, Optional

class JobRepositoryInterface(ABC):
    @abstractmethod
    def create(self, job: Job) -> Job:
        pass

    @abstractmethod
    def get_by_id(self, job_id: int) -> Optional[Job]:
        """
        The function `get_by_id` retrieves a job object based on its ID.
        
        :param job_id: The `job_id` parameter in the `get_by_id` method is of type `int`, representing
        the unique identifier of a job
        :type job_id: int
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Job]:
        pass

    @abstractmethod
    def search(self, filters: dict) -> List[Job]:
        pass

    @abstractmethod
    def update(self, job: Job) -> Job:
        pass

    @abstractmethod
    def delete(self, job_id: int) -> bool:
        pass