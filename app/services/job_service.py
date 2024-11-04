from typing import List
from app.common.exceptions.base_exception import InvalidDataException
from app.common.logger import logger
from app.common.dtos.job_dto import CreateJobDTO, JobResponseDTO, JobSearchDTO
from app.domains.skill_domain import SkillDomain
from app.enums.job_source_type import JobSourceType
from app.events.interfaces.event_publisher import EventPublisher
from app.interfaces.job_repository_interface import JobRepositoryInterface
from app.common.mappers.job_mapper import JobMapper
from app.common.utils.hash_util import JobHashService
from app.common.exceptions.job_exceptions import DuplicateJobException, InvalidSearchException

class JobService:
    def __init__(self, job_repository: JobRepositoryInterface, event_publisher: EventPublisher):
        self.job_repository = job_repository
        self.event_publisher = event_publisher
        
    def create_external_jobs(self, createInternalJobDto: CreateJobDTO) -> int:
        createInternalJobDto["source_type"] = JobSourceType.EXTERNAL
        return self._create_jobs(createInternalJobDto)

    def create_internal_jobs(self, createInternalJobDto: CreateJobDTO) -> int:
        createInternalJobDto["source_type"] = JobSourceType.INTERNAL
        return self._create_jobs(createInternalJobDto)

    def _create_jobs(self, createJobDto: CreateJobDTO) -> int:
        job_hash = JobHashService.generate_job_hash(createJobDto)

        if self.job_repository.exists_job_hash(job_hash):
            raise DuplicateJobException("job already exist")
        
        job = JobMapper.from_create_job_DTO_to_job_domain(createJobDto)
        job.job_hash = job_hash

        try:
            job.skills = self._get_or_create_skills(createJobDto['skills'])

            created_job = self.job_repository.create(job)

            event = JobMapper.from_job_domain_to_event(created_job)

            self.event_publisher.publish(event)
            return created_job.id

        except Exception as e:
            logger.error(f"Error in job creation process: {str(e)}")
            raise InvalidDataException(f"Failed to create job")
        
    def search_jobs(self, filters: JobSearchDTO) -> List[JobResponseDTO]:
        try:
            jobs = self.job_repository.search_jobs(filters)
            return JobMapper.from_jobs_domain_to_jobResponseDTOs(jobs)
        except Exception as e:
            logger.error(f"Error in job search process: {str(e)}")
            raise InvalidSearchException(f"Failed to search job")
        
    def _get_or_create_skills(self, skill_names: List[str]) -> List[SkillDomain]:
        skills = []
        for name in skill_names:
            skill = self.job_repository.get_or_create_skill(name)
            skills.append(skill)
        return skills
