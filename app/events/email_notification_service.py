from typing import Any
from app.interfaces.notification_service_interface import NotificationServiceInterface
from app.tasks.notification_task import notify_user
from app.common.logger import logger
from concurrent.futures import ThreadPoolExecutor

class EmailNotificationService(NotificationServiceInterface):
    def __init__(self, app):
        self._executor = ThreadPoolExecutor(max_workers=3)
        self.app = app 

    def notify(self, email: str, job_data: dict) -> None:
        self._executor.submit(self._send_notification, email, job_data)

    def _send_notification(self, email: str, job_data: dict) -> None:
        with self.app.app_context():
            try:
                notify_user.apply_async(
                    args=[email, job_data],
                    retry=False,
                    ignore_result=True
                )
            except Exception as e:
                logger.error(f"Error queuing notification for {email}: {str(e)}")
