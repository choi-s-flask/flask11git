from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import User, db

users_blp = Blueprint('users', __name__)

@users_blp.route('/', methods=['GET'])
def connect():
    return jsonify({"message": "Success Connect"})

@users_blp.route('/signup', methods=['POST'])
def signup_page():
    data = request.get_json()
    #필수 항목 확인
    required_fields =['name', 'email', 'age', 'gender']
    missing = [field for field in required_fields if field not in data]

    if missing:
            return jsonify({
                    "message": f"다음 항목이 누락되었습니다: {', '.join(missing)}"
            }), 400
    # 이메일 중복 체크
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
            return jsonify({
                    "message": "이미 등록된 이메일입니다"
            }), 400
    # 회원 생성
    user =User(

    name = data['name'],
    email = data['email'],
    age = data['age'],
    gender = data['gender'],
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": f"{user.name}님 회원가입을 축하드립니다",
        "user_id": user.id
    }), 201

