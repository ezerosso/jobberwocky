import unittest
from app.common.dtos.job_dto import JobSearchDTO
from app.domains.job_domain import JobDomain
from app.domains.skill_domain import SkillDomain
from app.repositories.in_memory_job_repository import InMemoryJobRepository

class TestInMemoryJobRepository(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryJobRepository()

    def test_create_job_without_skills(self):
        job = JobDomain(
            title="Software Engineer",
            location="Remote",
            salary=100000,
            company="TechCorp",
            skills=[]
        )

        with self.assertRaises(ValueError) as context:
            self.repo.create(job)
        
        self.assertEqual(str(context.exception), "The 'skills' field is required and cannot be empty.")
        
    def test_create_job_with_skills(self):
        skill1 = SkillDomain(id=1, name="Python")
        skill2 = SkillDomain(id=2, name="Django")

        job = JobDomain(
            title="Software Engineer",
            location="Remote",
            salary=100000,
            company="TechCorp",
            skills=[skill1, skill2]
        )

        created_job = self.repo.create(job)

        self.assertEqual(created_job.id, 1)
        self.assertEqual(created_job.title, "Software Engineer")
        self.assertEqual(created_job.salary, 100000)
        self.assertEqual(len(created_job.skills), 2)
        self.assertEqual(created_job.skills[0].name, "Python")
        self.assertEqual(created_job.skills[1].name, "Django")
        
        
    def test_get_or_create_skill(self):
        skill_name = "Python"
        skill = self.repo.get_or_create_skill(skill_name)

        self.assertEqual(skill.name, "Python")
        self.assertIn(skill_name, self.repo.skills)

        skill_again = self.repo.get_or_create_skill(skill_name)
        self.assertEqual(skill.id, skill_again.id)
        self.assertEqual(len(self.repo.skills), 1)
        
    def test_exists_job_hash(self):
        job = JobDomain(
            title="Backend Developer",
            location="Berlin",
            salary=90000,
            company="DevCorp",
            skills=[SkillDomain(id=4, name="Java")],
            job_hash="123abc"
        )
        self.repo.create(job)

        self.assertTrue(self.repo.exists_job_hash("123abc"))
        self.assertFalse(self.repo.exists_job_hash("nonexistenthash"))
        
    def test_search_jobs(self):
        job1 = JobDomain(
            title="Full Stack Developer",
            location="Remote",
            salary=95000,
            company="WebCorp",
            skills=[SkillDomain(id=1, name="React"), SkillDomain(id=2, name="JavaScript")]
        )
        job2 = JobDomain(
            title="Data Engineer",
            location="NYC",
            salary=110000,
            company="DataCorp",
            skills=[SkillDomain(id=3, name="Python"), SkillDomain(id=4, name="SQL")]
        )
        job3 = JobDomain(
            title="Backend Developer",
            location="Berlin",
            salary=90000,
            company="DevCorp",
            skills=[SkillDomain(id=5, name="Java")]
        )

        self.repo.create(job1)
        self.repo.create(job2)
        self.repo.create(job3)
        
        filters_data = {
            "title": "developer",
            "location": "remote",
            "salary_min": 90000,
            "skills": ["Python"]
        }

        filters = JobSearchDTO().load(filters_data)

        results = self.repo.search_jobs(filters)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Full Stack Developer")

if __name__ == "__main__":
    unittest.main()
