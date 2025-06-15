# from datetime import datetime
# from config import db
# import enum
#
# class CommonModel(db.Model):
#     __abstract__ = True
#
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#
# class Gender(enum.Enum):
#     male = 'male'
#     female = 'female'
#
# class User(CommonModel):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(10), nullable=False)
#     age = db.Column(
#         db.Enum(
#             'teen',
#             'twenty',
#             'thirty',
#             'forty',
#             'fifty',
#             name='age_enum'
#         ),
#         nullable=False
#     )
#     gender = db.Column(db.Enum(Gender, name='gender_enum'), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     # created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
# class Image(CommonModel):
#     __tablename__ = 'images'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     url = db.Column(db.String(255), nullable=False)
#     type = db.Column(
#         db.Enum(
#             'main',
#             'sub',
#             name='image_type_enum'
#         ),
#         nullable=False
#     )
#     # created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#
# class Question(CommonModel):
#     __tablename__ = 'questions'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
#     title = db.Column(db.String(100), nullable=False)
#     sqe = db.Column(db.Integer, nullable=False)
#     is_active = db.Column(db.Boolean, nullable=False, default=True)
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'image_id': self.image_id,
#             'title': self.title,
#             'sqe': self.sqe,
#             'is_active': self.is_active,
#         }
#
# class Choices(CommonModel):
#     __tablename__ = 'choices'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
#     content = db.Column(db.String(255), nullable=False)
#     sqe = db.Column(db.Integer, nullable=False)
#     is_active = db.Column(db.Boolean, nullable=False, default=True)
#     # created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "content": self.content,
#             "is_active": self.is_active,
#             "sqe": self.sqe,
#             "question_id": self.question_id,
#         }
#
# class Answer(CommonModel):
#     __tablename__ = 'answers'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'), nullable=False)
#     # created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo

from config import db

KST = ZoneInfo("Asia/Seoul")


class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(tz=KST), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(tz=KST),
        onupdate=lambda: datetime.now(tz=KST),
        nullable=False,
    )


class AgeStatus(Enum):
    teen = "teen"
    twenty = "twenty"
    thirty = "thirty"
    forty = "forty"
    fifty = "fifty"


class GenderStatus(Enum):
    male = "male"
    female = "female"


class ImageStatus(Enum):
    main = "main"
    sub = "sub"


class User(CommonModel):
    __tablename__ = "users"
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Enum(AgeStatus), nullable=False)
    gender = db.Column(db.Enum(GenderStatus), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age.value if hasattr(self.age, "value") else self.age,
            "gender": (
                self.gender.value if hasattr(self.gender, "value") else self.gender
            ),
            "email": self.email,
        }


class Image(CommonModel):
    __tablename__ = "images"
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(ImageStatus), nullable=False)

    questions = db.relationship("Question", back_populates="image")

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type.value if hasattr(self.type, "value") else self.type,
        }


class Question(CommonModel):
    __tablename__ = "questions"
    title = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    sqe = db.Column(db.Integer, nullable=False)

    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)

    image = db.relationship("Image", back_populates="questions")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "choices": [choice.to_dict() for choice in sorted(self.choices, key=lambda c: c.sqe)]
        }

class Choices(CommonModel):
    __tablename__ = "choices"
    content = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    sqe = db.Column(db.Integer, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_active": self.is_active,
            "sqe": self.sqe,
            "question_id": self.question_id,
        }


class Answer(CommonModel):
    __tablename__ = "answers"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    choice_id = db.Column(db.Integer, db.ForeignKey("choices.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "choice_id": self.choice_id,
        }