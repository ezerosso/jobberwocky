from concurrent.futures import ThreadPoolExecutor
from typing import List
from app.common.logger import logger
from app.events.interfaces.event_subscriber import EventSubscriber
from app.interfaces.notification_service_interface import NotificationServiceInterface
from app.utils.search_matcher import SearchMatcher

class JobNotificationSubscriber(EventSubscriber):
    def __init__(self, subscriber_repository, notification_services: List[NotificationServiceInterface], app):
        self.subscriber_repository = subscriber_repository
        self.notification_services = notification_services
        self._executor = ThreadPoolExecutor(max_workers=5)
        self.app = app

    def handle(self, event: EventSubscriber) -> None:
        self._executor.submit(self._process_event, event)
        
    def _process_event(self, event: EventSubscriber) -> None:
        with self.app.app_context() :
            job_data = {
                'title': event.title,
                'company': event.company,
                'location': event.location,
                'skills': event.skills,
            }

            try:
                active_subscribers = self.subscriber_repository.get_all_active_subscribers()
                for subscriber in active_subscribers:
                    if SearchMatcher.matches_pattern(job_data, subscriber.search_pattern):
                        self._notify_subscriber(subscriber.email, job_data)
            except Exception as e:
                logger.error(f"Error processing job notification event: {str(e)}")

    def _notify_subscriber(self, email: str, job_data: dict) -> None:
        for service in self.notification_services:
            try:
                service.notify(email, job_data)
            except Exception as e:
                logger.error(f"Error notifying {email} using {service}: {e}")