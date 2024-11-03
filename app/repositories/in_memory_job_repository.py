from app.common.dtos.job_dto import JobSearchDTO
from app.interfaces.job_repository_interface import JobRepositoryInterface
from app.models.job import Job
from app.models.skill import Skill
from typing import List, Dict, Optional

class InMemoryJobRepository(JobRepositoryInterface):
    def __init__(self):
        self.jobs: Dict[int, Job] = {}
        self.skills: Dict[str, Skill] = {}
        self.next_id = 1

    def create(self, job: Job) -> Job:
        job.id = self.next_id
        self.jobs[self.next_id] = job
        self.next_id += 1
        return job

    def get_all(self) -> List[Job]:
        return list(self.jobs.values())

    def find_by_id(self, job_id: int) -> Optional[Job]:
        return self.jobs.get(job_id)

    def search_jobs(self, filters: JobSearchDTO) -> List[Job]:
        # Implement search logic here
        pass

    def get_or_create_skill(self, skill_name: str) -> Skill:
        if skill_name not in self.skills:
            skill = Skill(name=skill_name)
            self.skills[skill_name] = skill
        return self.skills[skill_name]

    def exists_job_hash(self, job_hash: str) -> bool:
        for job in self.jobs.values():
            if job.hash == job_hash:
                return True
        return False