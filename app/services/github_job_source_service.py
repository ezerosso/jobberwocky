from typing import Dict, List
import requests
from app.common.dtos.job_dto import CreateJobDTO
from app.interfaces.external_job_service_interface import ExternalJobSourceInterface
from app.common.logger import logger
from xml.etree import ElementTree as ET

class GithubJobsSource(ExternalJobSourceInterface):
    def __init__(self, url: str):
        self.url = url

    def fetch_jobs(self) -> List[Dict]:
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            external_jobs = response.json()
            return self._transform_jobs(external_jobs)
        except requests.RequestException as e:
            logger.error(f"Error fetching jobs from {self.url}: {e}")
            return []
        
    def _transform_jobs(self, external_jobs: List[Dict]) -> List[CreateJobDTO]:
        transformed_jobs = []
        
        data = external_jobs
        
        for country, jobs in data.items():
            for job_info in jobs:
                title = job_info[0]
                salary = job_info[1]
                
                skills_xml = job_info[2]
                skills = extract_skills_from_xml(skills_xml)
                
                job_dict = {
                    "title": title,
                    "salary": salary,
                    "company": "external company",  
                    "location": country, 
                    "skills": skills,
                }
                
                job_dto = CreateJobDTO().load(job_dict)
                transformed_jobs.append(job_dto)

        return transformed_jobs

def extract_skills_from_xml(xml_string):
    root = ET.fromstring(xml_string)
    return [skill.text for skill in root.findall('skill')]