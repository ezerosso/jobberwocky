import unittest
from unittest.mock import MagicMock

from requests import patch
from app.common.dtos.job_dto import CreateJobDTO, JobSearchDTO
from app.common.exceptions.base_exception import InvalidDataException
from app.common.exceptions.job_exceptions import DuplicateJobException, InvalidSearchException
from app.models.job import Job
from app.repositories.in_memory_job_repository import InMemoryJobRepository
from app.services.job_service import JobService

class TestJobService(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryJobRepository()
        self.event_publisher = MagicMock()
        self.job_service = JobService(self.repository, self.event_publisher)

    def test_create_external_jobs_success(self):
        job_dto = CreateJobDTO(
            title="Software Engineer",
            company="Tech Co",
            location="Remote",
            skills=["Python", "Django"]
        )
        job_id = self.job_service.create_external_jobs(job_dto)
        self.assertEqual(job_id, 1)
        self.assertEqual(len(self.repository.jobs), 1)
        self.event_publisher.publish.assert_called_once()

    def test_create_external_jobs_duplicate(self):
        job_dto = CreateJobDTO(
            title="Software Engineer",
            company="Tech Co",
            location="Remote",
            skills=["Python", "Django"]
        )
        self.repository.create(Job(job_hash="12345"))  # Add job with the same hash to simulate duplicate

        with self.assertRaises(DuplicateJobException):
            self.job_service.create_external_jobs(job_dto)

    def test_create_jobs_invalid_data_exception(self):
        job_dto = CreateJobDTO(
            title="Software Engineer",
            company="Tech Co",
            location="Remote",
            skills=["Python", "Django"]
        )
        with patch('app.utils.hash_util.JobHashService.generate_job_hash', side_effect=Exception("Error")):
            with self.assertRaises(InvalidDataException):
                self.job_service.create_external_jobs(job_dto)

    def test_search_jobs_success(self):
        filters = JobSearchDTO(
            title="Software Engineer",
            company="Tech Co"
        )
        self.repository.create(Job(title="Software Engineer", company="Tech Co"))
        results = self.job_service.search_jobs(filters)
        self.assertGreaterEqual(len(results), 1)

    def test_search_jobs_invalid_search_exception(self):
        filters = JobSearchDTO(title="Non-existent")
        with patch('app.interfaces.job_repository_interface.JobRepositoryInterface.search_jobs', side_effect=Exception("Error")):
            with self.assertRaises(InvalidSearchException):
                self.job_service.search_jobs(filters)

if __name__ == '__main__':
    unittest.main()