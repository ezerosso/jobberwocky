from typing import List
from app.interfaces.external_job_service_interface import ExternalJobSourceInterface
from app.services.job_service import JobService
from app.common.logger import logger

class ExternalJobService:
    def __init__(self, sources: List[ExternalJobSourceInterface], job_service: JobService):
        self.sources = sources
        self.job_service = job_service

    def fetch_and_save_jobs(self):
        for source in self.sources:
            try:
                job_dtos = source.fetch_jobs()
                for job_dto in job_dtos:
                    try:
                        self.job_service.create_external_jobs(job_dto)
                    except Exception as job_error:
                        logger.error(f"Error saving job {job_dto}: {job_error}")
            except Exception as source_error:
                logger.error(f"Error processing source {source}: {source_error}")
