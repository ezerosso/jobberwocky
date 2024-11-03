from app.interfaces.subscriber_repository_interface import SubscriberRepositoryInterface
from app.models.subscriber import Subscriber
from typing import List, Dict, Optional

class InMemorySubscriberRepository(SubscriberRepositoryInterface):
    def __init__(self):
        self.subscribers: Dict[int, Subscriber] = {}
        self.email_index: Dict[str, int] = {}
        self.next_id = 1

    def create(self, subscriber: Subscriber) -> Subscriber:
        subscriber.id = self.next_id
        self.subscribers[self.next_id] = subscriber
        self.email_index[subscriber.email] = self.next_id
        self.next_id += 1
        return subscriber

    def get_all(self) -> List[Subscriber]:
        return list(self.subscribers.values())

    def find_by_id(self, subscriber_id: int) -> Optional[Subscriber]:
        return self.subscribers.get(subscriber_id)

    def find_by_email(self, email: str) -> Optional[Subscriber]:
        subscriber_id = self.email_index.get(email)
        return self.subscribers.get(subscriber_id)
    
    def get_all_active_subscribers(self) -> List[Subscriber]:
        return list(self.subscribers.values())
    
    def exists_subscriber(self, subscriber: Subscriber) -> bool:
        for subscriberdb in self.subscribers.values():
            if subscriberdb.email == subscriber.email and subscriberdb.search_pattern == subscriber.search_pattern:
                return True
        return False
