from typing import List, Optional


class JobDomain:
    def __init__(self, 
                 title: str, 
                 company: str, 
                 location: str, 
                 skills: List[str], 
                 job_hash: Optional[str] = None, 
                 id: Optional[int] = None,
                 source_type: Optional[str] = None,
                 salary: Optional[int] = None):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.skills = skills
        self.job_hash = job_hash
        self.source_type = source_type
        self.salary = salary