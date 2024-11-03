from typing import Dict, List
import requests
from app.interfaces.external_job_service_interface import ExternalJobSourceInterface
from app.common.logger import logger

class GithubJobsSource(ExternalJobSourceInterface):
    def __init__(self, url: str):
        self.url = url

    def fetch_jobs(self) -> List[Dict]:
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching jobs from {self.url}: {e}")
            return []