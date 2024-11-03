from typing import Dict, List, Type, Any
from app.events.interfaces.event_publisher import EventPublisher
from app.events.interfaces.event_subscriber import EventSubscriber
from app.common.logger import logger

class EventBus(EventPublisher):
    def __init__(self):
        self._subscribers: Dict[Type, List[EventSubscriber]] = {}

    def subscribe(self, event_type: Type, subscriber: EventSubscriber) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(subscriber)

    def publish(self, event: Any) -> None:
        event_type = type(event)
        if event_type in self._subscribers:
            for subscriber in self._subscribers[event_type]:
                try:
                    subscriber.handle(event)
                except Exception as e:
                    logger.info(f"Error handling event {event_type} by {subscriber}: {e}")