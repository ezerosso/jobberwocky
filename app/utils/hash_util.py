import hashlib

class JobHashService:
    @staticmethod
    def generate_job_hash(job_data: dict) -> str:
        sorted_skills = sorted(job_data['skills'])
        skills_str = ','.join(sorted_skills)

        hash_input = f"{job_data['title']}-{job_data['company']}-{job_data.get('salary')}-{job_data['location']}-{skills_str}"
        return hashlib.sha256(hash_input.encode()).hexdigest()