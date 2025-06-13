from datetime import datetime
from config import db
import enum

class CommonModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Gender(enum.Enum):
    male = 'male'
    female = 'female'

class User(CommonModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(
        db.Enum(
            'teen',
            'twenty',
            'thirty',
            'forty',
            'fifty',
            name='age_enum'
        ),
        nullable=False
    )
    gender = db.Column(db.Enum(Gender, name='gender_enum'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Image(CommonModel):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(
        db.Enum(
            'main',
            'sub',
            name='image_type_enum'
        ),
        nullable=False
    )
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Question(CommonModel):
        __tablename__ = 'questions'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
        title = db.Column(db.String(100), nullable=False)
        sqe = db.Column(db.Integer, nullable=False)
        is_active = db.Column(db.Boolean, nullable=False)

        def to_dict(self):
            return {
                'id': self.id,
                'image_id': self.image_id,
                'title': self.title,
                'sqe': self.sqe,
                'is_active': self.is_active,
            }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Choices(CommonModel):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Answer(CommonModel):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



