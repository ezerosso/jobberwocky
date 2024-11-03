from flask import current_app
from celery import shared_task

from app.common.logger import logger

@shared_task
def log_task():
    external_job_service = current_app.container.external_job_service
    if not external_job_service:
        return 0
    
    logger.info("tarea programada...")

    external_job_service.fetch_and_save_jobs()
    
