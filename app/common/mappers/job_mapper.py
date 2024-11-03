from typing import List

from app.common.dtos.job_dto import CreateJobDTO, JobResponseDTO, SubscriberDTO
from app.models.job import Job
import xml.etree.ElementTree as ET

from app.models.subscriber import Subscriber

class JobMapper:    
    @staticmethod
    def from_job_to_jobResponseDTO(job: Job) -> JobResponseDTO:
        return JobResponseDTO(
            title=job.title,
            salary=job.salary,
            company=job.company,
            location=job.location,
            skills=[job_skill.skill.name for job_skill in job.skills if job_skill.skill],
            source_type=job.source_type.name if job.source_type else None,
        )

    @staticmethod
    def from_jobs_to_jobResponseDTOs(jobs: List[Job]) -> List[JobResponseDTO]:
        return [JobMapper.from_job_to_jobResponseDTO(job) for job in jobs]
    
    @staticmethod
    def from_createInternalJobDTO_to_job(createInternalJobDTO: CreateJobDTO) -> Job:
        return Job(
            title=createInternalJobDTO.get('title'),
            salary=createInternalJobDTO.get('salary'),
            company=createInternalJobDTO.get('company'),
            location=createInternalJobDTO.get('location'),
            source_type = createInternalJobDTO.get('source_type'),
            hash = createInternalJobDTO.get('job_hash')
        )
        
    @staticmethod
    def from_SubscriberDTO_to_subscriber(subscriberDTO: SubscriberDTO) -> Job:
        return Subscriber(email=subscriberDTO['email'], search_pattern=subscriberDTO['pattern'])
        
    @staticmethod
    def from_import_data_to_create_dto(job_data: list, country: str) -> dict:
        title, salary, skills_xml = job_data
        
        # Parse XML skills
        try:
            root = ET.fromstring(skills_xml)
            skills = [skill.text for skill in root.findall('skill') if skill.text]
        except ET.ParseError:
            skills = []
        
        return {
            'title': title,
            'salary': salary,
            'location': country,
            'skills': skills,
            'source': 'EXTERNAL'
        }