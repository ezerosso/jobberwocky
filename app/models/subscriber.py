from app import db
from datetime import datetime

class Subscriber(db.Model):
    __tablename__ = 'subscriber'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    search_pattern = db.Column(db.String(100), nullable=False)
