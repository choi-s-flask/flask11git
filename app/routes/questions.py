from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Question(db.Model):
    tablename = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)