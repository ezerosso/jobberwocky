import json
from typing import List

class JobMapper:
    @staticmethod
    def from_external_api(data: dict) -> List[Job]:
        jobs = []
        for location, job_list in data.items():
            for job_data in job_list:
                job = Job(
                    id=None,  # Se asignará al guardar en DB
                    title=job_data[0],
                    salary=float(job_data[1]),
                    location=location,
                    skills=Job.parse_skills_xml(job_data[2])
                )
                jobs.append(job)
        return jobs

    @staticmethod
    def to_dict(job: Job) -> dict:
        return {
            "id": job.id,
            "title": job.title,
            "salary": job.salary,
            "location": job.location,
            "skills": job.skills,
        }