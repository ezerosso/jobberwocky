import datetime
from typing import List
from app.common.exceptions.base_exception import InvalidDataException
from app.common.logger import logger
from app.common.dtos.job_dto import CreateJobDTO, JobResponseDTO, JobSearchDTO
from app.enums.job_source_type import JobSourceType
from app.events.interfaces.event_publisher import EventPublisher
from app.events.job_created_event import JobCreatedEvent
from app.interfaces.job_repository_interface import JobRepositoryInterface
from app.common.mappers.job_mapper import JobMapper
from app.models.job_skill import JobSkill
from app.common.utils.hash_util import JobHashService

from app.common.decorators.transaction import transactional
from app.common.exceptions.job_exceptions import DuplicateJobException, InvalidSearchException

class JobService:
    def __init__(self, job_repository: JobRepositoryInterface, event_publisher: EventPublisher):
        self.job_repository = job_repository
        self.event_publisher = event_publisher
        
    @transactional
    def create_external_jobs(self, createInternalJobDto: CreateJobDTO) -> int:
        createInternalJobDto["source_type"] = JobSourceType.EXTERNAL
        return self._create_jobs(createInternalJobDto)

    @transactional
    def create_internal_jobs(self, createInternalJobDto: CreateJobDTO) -> int:
        createInternalJobDto["source_type"] = JobSourceType.INTERNAL
        return self._create_jobs(createInternalJobDto)

    @transactional
    def _create_jobs(self, createInternalJobDto: CreateJobDTO) -> int:
        job_hash = JobHashService.generate_job_hash(createInternalJobDto)

        if self.job_repository.exists_job_hash(job_hash):
            raise DuplicateJobException("job already exist")

        createInternalJobDto['job_hash'] = job_hash
        job = JobMapper.from_createInternalJobDTO_to_job(createInternalJobDto)

        try:
            for skill_name in createInternalJobDto['skills']:
                skill = self.job_repository.get_or_create_skill(skill_name)
                job.skills.append(JobSkill(job=job, skill=skill))

            created_job = self.job_repository.create(job)

            event = JobCreatedEvent(
                id=created_job.id,
                title=created_job.title,
                company=created_job.company,
                location=created_job.location,
                skills=[job_skill.skill.name for job_skill in created_job.skills if job_skill.skill],
                created_at=datetime.datetime.now()
            )

            self.event_publisher.publish(event)
            return created_job.id

        except Exception as e:
            logger.error(f"Error in job creation process: {str(e)}")
            raise InvalidDataException(f"Failed to create job")
        
    def search_jobs(self, filters: JobSearchDTO) -> List[JobResponseDTO]:
        try:
            jobs = self.job_repository.search_jobs(filters)
            return JobMapper.from_jobs_to_jobResponseDTOs(jobs)
        except Exception as e:
            logger.error(f"Error in job search process: {str(e)}")
            raise InvalidSearchException(f"Failed to search job")
