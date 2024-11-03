from abc import abstractmethod
from app.interfaces.generic_repository_interface import GenericRepositoryInterface
from app.models.subscriber import Subscriber
from typing import List

class SubscriberRepositoryInterface(GenericRepositoryInterface[Subscriber]):
    @abstractmethod
    def get_all_active_subscribers(self) -> List[Subscriber]:
        pass
    
    @abstractmethod
    def exists_subscriber(self, subscriber: Subscriber) -> bool:
        pass
    
