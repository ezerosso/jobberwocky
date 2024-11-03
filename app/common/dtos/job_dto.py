
from dataclasses import dataclass
from typing import List, Optional
from marshmallow import Schema, fields

from app.enums.job_source_type import JobSourceType

class CreateJobDTO(Schema):
    title = fields.String(required=True, validate=lambda e: e.strip() != "")
    salary = fields.Integer(required=False)
    company = fields.String(required=True, validate=lambda e: e.strip() != "")
    location = fields.String(required=True, validate=lambda e: e.strip() != "")
    skills = fields.List(fields.String(), required=True)
    source_type = fields.String(required=False)
    hash= fields.String(required=False)
    
class JobSearchDTO(Schema):
    title = fields.Str(required=False)
    location = fields.Str(required=False)
    salary_min = fields.Float(required=False)
    salary_max = fields.Float(required=False)
    skills = fields.List(fields.Str(), required=False)
    
@dataclass
class JobResponseDTO:
    title: str
    company: str
    salary: Optional[int] = None
    location: Optional[str] = None
    skills: List[str] = None
    source_type: JobSourceType = None

class SubscriberDTO(Schema):
    email = fields.Email(required=True, validate=lambda e: e.strip() != "", error_messages={"required": "email is required"})
    pattern = fields.Str(required=True, validate=lambda e: e.strip() != "")
