from app.interfaces.job_repository_interface import JobRepositoryInterface
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.skill import Skill
from app import db
from sqlalchemy.orm import joinedload
from typing import List, Optional

class SQLiteJobRepository(JobRepositoryInterface):
    def create(self, job: Job) -> Job:
        db.session.add(job)
        db.session.commit()
        return job

    def get_all(self) -> List[Job]:
        return Job.query.all()

    def find_by_id(self, job_id: int) -> Optional[Job]:
        return Job.query.get(job_id)

    def search_jobs(self, filters: dict = None):
        query = Job.query.options(joinedload(Job.skills))

        if filters:
            if "title" in filters:
                query = query.filter(Job.title.ilike(f"%{filters['title']}%"))
            if "location" in filters:
                query = query.filter(Job.location.ilike(f"%{filters['location']}%"))
            if "salary_min" in filters:
                query = query.filter(Job.salary >= filters["salary_min"])
            if "salary_max" in filters:
                query = query.filter(Job.salary <= filters["salary_max"])
            if "skills" in filters and filters["skills"]:
                query = query.join(JobSkill).join(Skill).filter(Skill.name.in_(filters["skills"]))

        return query.all()

    def get_or_create_skill(self, skill_name: str) -> Skill:
        skill = Skill.query.filter_by(name=skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)
            db.session.commit()
        return skill

    def exists_job_hash(self, job_hash: str) -> bool:
        return db.session.query(Job).filter_by(hash=job_hash).first() is not None