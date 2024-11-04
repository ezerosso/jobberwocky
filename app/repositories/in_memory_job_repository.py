from app.common.dtos.job_dto import JobSearchDTO
from app.domains.job_domain import JobDomain
from app.domains.skill_domain import SkillDomain
from app.interfaces.job_repository_interface import JobRepositoryInterface
from typing import List, Dict, Optional

class InMemoryJobRepository(JobRepositoryInterface):
    def __init__(self):
        self.jobs: Dict[int, JobDomain] = {}
        self.skills: Dict[str, SkillDomain] = {}
        self.next_id = 1

    def create(self, job: JobDomain) -> JobDomain:
        if not job.skills:
            raise ValueError("The 'skills' field is required and cannot be empty.")
        job.id = self.next_id
        self.jobs[self.next_id] = job
        self.next_id += 1
        return job

    def get_all(self) -> List[JobDomain]:
        return list(self.jobs.values())

    def find_by_id(self, job_id: int) -> Optional[JobDomain]:
        return self.jobs.get(job_id)

    def search_jobs(self, filters: JobSearchDTO) -> List[JobDomain]:
        results = list(self.jobs.values())
        
        if filters:
            if "title" in filters and filters["title"]:
                results = [job for job in results if filters["title"].lower() in job.title.lower()]

            if "location" in filters and filters["location"]:
                results = [job for job in results if filters["location"].lower() in job.location.lower()]

            if "salary_min" in filters and filters["salary_min"] is not None:
                results = [job for job in results if job.salary is not None and job.salary >= filters["salary_min"]]

            if "salary_max" in filters and filters["salary_max"] is not None:
                results = [job for job in results if job.salary is not None and job.salary <= filters["salary_max"]]

        return [JobDomain(
            id=job.id,
            title=job.title,
            location=job.location,
            salary=job.salary,
            company=job.company,
            skills=job.skills
        ) for job in results]

    def get_or_create_skill(self, skill_name: str) -> SkillDomain:
        if skill_name not in self.skills:
            skill_id = len(self.skills) + 1
            skill = SkillDomain(id=skill_id, name=skill_name)
            self.skills[skill_name] = skill
        return self.skills[skill_name]

    def exists_job_hash(self, job_hash: str) -> bool:
        for job in self.jobs.values():
            if job.job_hash == job_hash:
                return True
        return False