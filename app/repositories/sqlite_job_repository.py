from app.common.logger import logger
from app.common.mappers.job_mapper import JobMapper
from app.domains.job_domain import JobDomain
from app.domains.skill_domain import SkillDomain
from app.interfaces.job_repository_interface import JobRepositoryInterface
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.skill import Skill
from app import db
from sqlalchemy.orm import joinedload
from typing import List, Optional

class SQLiteJobRepository(JobRepositoryInterface):
    def create(self, jobDomain: JobDomain) -> JobDomain:
        job_model = JobMapper.from_job_domain_to_job(jobDomain)
        
        try:
            db.session.add(job_model)
            db.session.commit()

            for skill in jobDomain.skills:
                    job_skill = JobSkill(job_id=job_model.id, skill_id=skill.id)
                    db.session.add(job_skill)

            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error while creating job: {e}")
            raise e

        return JobMapper.from_job_to_job_domain(job_model)

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

        return JobMapper.from_jobs_to_jobs_domain(query.all())

    def get_or_create_skill(self, skill_name: str) -> SkillDomain:
        skill = db.session.query(Skill).filter_by(name=skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)
            db.session.commit()
        return SkillDomain(id=skill.id, name=skill.name)

    def exists_job_hash(self, job_hash: str) -> bool:
        return db.session.query(Job).filter_by(hash=job_hash).first() is not None