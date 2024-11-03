from abc import abstractmethod
from app.interfaces.generic_repository_interface import GenericRepositoryInterface
from app.common.dtos.job_dto import JobSearchDTO
from app.models.job import Job
from app.models.skill import Skill
from typing import List

class JobRepositoryInterface(GenericRepositoryInterface[Job]):
    @abstractmethod
    def search_jobs(self, filters: JobSearchDTO) -> List[Job]:
        pass
    
    @abstractmethod
    def get_or_create_skill(self, skill_name: str) -> Skill:
        pass
    
    @abstractmethod
    def exists_job_hash(self, job_hash:str) -> bool:
        pass
