from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class GenericRepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[T]:
        pass