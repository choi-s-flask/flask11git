from flask import Flask
from datetime import datetime
import enum
from sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Gender(enum.Enum):
    male ='male'
    female ='female'

class User(db.Model):
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
    gender = db.Column(db.Enum(Gender.male,Gender.female,name='gender_enum'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)