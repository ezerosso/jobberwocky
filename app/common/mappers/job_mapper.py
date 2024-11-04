import datetime
from typing import List

from app.common.dtos.job_dto import CreateJobDTO, JobResponseDTO, SubscriberDTO
from app.domains.job_domain import JobDomain
from app.domains.skill_domain import SkillDomain
from app.events.job_created_event import JobCreatedEvent
from app.models.job import Job

from app.models.subscriber import Subscriber

class JobMapper:    
    @staticmethod
    def from_job_domain_to_jobResponseDTO(job: JobDomain) -> JobResponseDTO:
        return JobResponseDTO(
            title=job.title,
            salary=job.salary,
            company=job.company,
            location=job.location,
            skills=[skill.name for skill in job.skills],
            source_type=job.source_type.name if job.source_type else None,
        )

    @staticmethod
    def from_jobs_domain_to_jobResponseDTOs(jobs: List[JobDomain]) -> List[JobResponseDTO]:
        return [JobMapper.from_job_domain_to_jobResponseDTO(job) for job in jobs]
    
    @staticmethod
    def from_create_job_DTO_to_job_domain(createJobDto: CreateJobDTO) -> JobDomain:
        return JobDomain(
            title=createJobDto.get('title'),
            company=createJobDto.get('company'),
            location=createJobDto.get('location'),
            skills=createJobDto.get('skills'),
            salary=createJobDto.get('salary'),
            source_type=createJobDto.get('source_type'),
        )
        
    @staticmethod
    def from_job_to_job_domain(job_model: Job) -> JobDomain:
        skills = [SkillDomain(name=job_skill.skill.name, id=job_skill.skill.id) for job_skill in job_model.skills]
        
        return JobDomain(
            id=job_model.id,
            title=job_model.title,
            company=job_model.company,
            location=job_model.location,
            salary=job_model.salary,
            source_type=job_model.source_type,
            job_hash=job_model.hash,
            skills=skills
        )
        
    @staticmethod
    def from_jobs_to_jobs_domain (jobs : List[Job]) -> List[JobDomain]:
        return [JobMapper.from_job_to_job_domain(job) for job in jobs]
        
    @staticmethod
    def from_job_domain_to_job(job: JobDomain) -> Job:
        return Job(
            title=job.title,
            company=job.company,
            location=job.location,
            salary=job.salary,
            source_type=job.source_type,
            hash=job.job_hash
        )
        
    @staticmethod
    def from_job_domain_to_event(job: JobDomain) -> JobCreatedEvent:
        return JobCreatedEvent(
                    id=job.id,
                    title=job.title,
                    company=job.company,
                    location=job.location,
                    skills=[skill.name for skill in job.skills],
                    created_at=datetime.datetime.now()
                )
        