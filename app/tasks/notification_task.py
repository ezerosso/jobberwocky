from celery import shared_task
from celery.contrib.abortable import AbortableTask
from app.common.logger import logger

@shared_task(
    bind=True,
    base=AbortableTask,
    ignore_result=True,
    acks_late=True,
    reject_on_worker_lost=True
)
def notify_user(self, email, job_data):
    try:
        logger.info(f"send notification to: {email}, work: {job_data}")
    except Exception as e:
        logger.error(f"Error en notify_user para {email}: {str(e)}")