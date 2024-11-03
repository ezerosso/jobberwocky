from typing import List
from app.common.dtos.job_dto import CreateJobDTO
from app.interfaces.external_job_service_interface import ExternalJobSourceInterface
from app.services.job_service import JobService
from xml.etree import ElementTree as ET

from app.common.logger import logger

class ExternalJobService:

    def __init__(self, sources: List[ExternalJobSourceInterface], job_service: JobService):
        self.sources = sources
        self.job_service = job_service

    def fetch_and_save_jobs(self):
        saved_jobs = []
        for source in self.sources:
            try:
                raw_jobs = source.fetch_jobs()
                self.parse_jobs(raw_jobs)
            
            except Exception as source_error:
                logger.error(f"Error processing source {source}: {source_error}")
        
        return saved_jobs

    def parse_jobs(self, json_data):
        jobs_schema = CreateJobDTO()
        job_list = []
        
        data = json_data

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
                
                result = jobs_schema.load(job_dict) 
                self.job_service.create_external_jobs(result)
        
        return job_list

def extract_skills_from_xml(xml_string):
    root = ET.fromstring(xml_string)
    return [skill.text for skill in root.findall('skill')]