import unittest
from unittest.mock import MagicMock

from app.common.dtos.job_dto import CreateJobDTO
from app.enums.job_source_type import JobSourceType
from app.models.job import Job
from app.repositories.in_memory_job_repository import InMemoryJobRepository
from app.services.job_service import JobService

class TestJobService(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryJobRepository()
        self.event_publisher = MagicMock()
        self.job_service = JobService(self.repository, self.event_publisher)

    def test_create_external_jobs_success(self):
        job_dto = {
            "title": "Software Engineer",
            "company": "Tech Co",
            "location": "remote",
            "salary": 90000,
            "skills": ["Python", "Django"]
        }

        create_job_dto = CreateJobDTO().load(job_dto)

        job_id = self.job_service.create_external_jobs(create_job_dto)
        self.assertEqual(job_id, 1)
        self.assertEqual(len(self.repository.jobs), 1)
        created_job = self.repository.jobs[1]
        self.assertEqual(created_job.source_type, JobSourceType.EXTERNAL)
        self.assertEqual(created_job.title, "Software Engineer")
        self.assertEqual(len(created_job.skills), 2)
        self.event_publisher.publish.assert_called_once()
        
    def test_create_internal_jobs_success(self):
        job_dto = {
            "title": "Software Engineer",
            "location": "remote",
            "salary": 90000,
            "company": "external company",
            "skills": ["Python", "Java", "SQL"]
        }

        create_job_dto = CreateJobDTO().load(job_dto)

        job_id = self.job_service.create_internal_jobs(create_job_dto)
        self.assertEqual(job_id, 1)
        self.assertEqual(len(self.repository.jobs), 1)
        created_job = self.repository.jobs[1]
        self.assertEqual(created_job.source_type, JobSourceType.INTERNAL)
        self.assertEqual(created_job.title, "Software Engineer")
        self.assertEqual(len(created_job.skills), 3)
        self.event_publisher.publish.assert_called_once()
        

if __name__ == '__main__':
    unittest.main()