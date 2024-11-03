from functools import lru_cache
from typing import List

from flask import Flask

from app.core.config import AppConfig
from app.events.interfaces.event_publisher import EventPublisher
from app.events.event_bus import EventBus
from app.events.job_created_event import JobCreatedEvent
from app.repositories.sqlite_job_repository import SQLiteJobRepository
from app.repositories.sqlite_subscriber_repository import SQLiteSubscriberRepository
from app.events.email_notification_service import EmailNotificationService
from app.services.external_job_service import ExternalJobService
from app.services.github_job_source_service import GithubJobsSource
from app.services.job_service import JobService
from app.events.job_notification_subscriber import JobNotificationSubscriber
from app.services.subscriber_service import SubscriberService

class Container:
    def __init__(self, config: AppConfig, app: Flask):
        self.config = config
        self._instances = {}
        self.app = app
        _ = self.job_notification_subscriber

    @property
    @lru_cache()
    def event_bus(self) -> EventPublisher:
        if 'event_bus' not in self._instances:
            self._instances['event_bus'] = EventBus()
        return self._instances['event_bus']

    @property
    @lru_cache()
    def job_repository(self) -> SQLiteJobRepository:
        if 'job_repository' not in self._instances:
            self._instances['job_repository'] = SQLiteJobRepository()
        return self._instances['job_repository']

    @property
    @lru_cache()
    def subscriber_repository(self) -> SQLiteSubscriberRepository:
        if 'subscriber_repository' not in self._instances:
            self._instances['subscriber_repository'] = SQLiteSubscriberRepository()
        return self._instances['subscriber_repository']

    @property
    @lru_cache()
    def notification_services(self) -> List[EmailNotificationService]:
        if 'notification_services' not in self._instances:
            self._instances['notification_services'] = [
                EmailNotificationService(app=self.app),
            ]
        return self._instances['notification_services']

    @property
    @lru_cache()
    def job_notification_subscriber(self) -> JobNotificationSubscriber:
        if 'job_notification_subscriber' not in self._instances:
            subscriber = JobNotificationSubscriber(
                subscriber_repository=self.subscriber_repository,
                notification_services = self.notification_services,
                app=self.app
            )
            self.event_bus.subscribe(JobCreatedEvent, subscriber)
            self._instances['job_notification_subscriber'] = subscriber
        return self._instances['job_notification_subscriber']

    @property
    @lru_cache()
    def job_service(self) -> JobService:
        if 'job_service' not in self._instances:
            self._instances['job_service'] = JobService(
                job_repository=self.job_repository,
                event_publisher=self.event_bus
            )
        return self._instances['job_service']
    
    @property
    @lru_cache()
    def subscriber_service(self) -> SubscriberService:
        if 'subscriber_service' not in self._instances:
            self._instances['subscriber_service'] = SubscriberService(
                subscriber_repository=self.subscriber_repository
            )
        return self._instances['subscriber_service']

    @property
    @lru_cache()
    def github_jobs_source(self) -> GithubJobsSource:
        if 'github_jobs_source' not in self._instances:
            self._instances['github_jobs_source'] = GithubJobsSource(
                url=self.config.GITHUB_JOBS_URL
            )
        return self._instances['github_jobs_source']

    @property
    @lru_cache()
    def external_job_service(self) -> ExternalJobService:
        if 'external_job_service' not in self._instances:
            self._instances['external_job_service'] = ExternalJobService(
                sources=[self.github_jobs_source],
                job_service=self.job_service
            )
        return self._instances['external_job_service']

    def __del__(self):
        self._instances.clear()