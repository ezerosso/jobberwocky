from app import db

class JobSkill(db.Model):
    __tablename__ = 'job_skills'

    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)

    job = db.relationship('Job', back_populates='skills')
    skill = db.relationship('Skill', back_populates='jobs')