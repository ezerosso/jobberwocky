from datetime import datetime
from app import db
from app.enums.job_source_type import JobSourceType
class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    source_type = db.Column(db.Enum(JobSourceType), nullable=True) 
    hash = db.Column(db.String(64), unique=True, nullable=False)

    skills = db.relationship('JobSkill', back_populates='job')

    def __repr__(self):
        return f"<Job(title='{self.title}', salary={self.salary}, company='{self.company}')>"
