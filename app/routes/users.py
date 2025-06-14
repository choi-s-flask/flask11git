# from flask import Blueprint, request, jsonify
# from app.models import User, db
#
# users_blp = Blueprint('users', __name__)
#
# @users_blp.route('/', methods=['GET'])
# def connect():
#     return jsonify({"message": "Success Connect"})
#
# @users_blp.route('/signup', methods=['POST'])
# def signup_page():
#     data = request.get_json()
#     #필수 항목 확인
#     required_fields =['name', 'email', 'age', 'gender']
#     missing = [field for field in required_fields if field not in data]
#
#     if missing:
#             return jsonify({
#                     "message": f"다음 항목이 누락되었습니다: {', '.join(missing)}"
#             }), 400
#     # 이메일 중복 체크
#     existing_user = User.query.filter_by(email=data['email']).first()
#     if existing_user:
#             return jsonify({
#                     "message": "이미 등록된 이메일입니다"
#             }), 400
#     # 회원 생성
#     user =User(
#
#     name = data['name'],
#     email = data['email'],
#     age = data['age'],
#     gender = data['gender'],
#     )
#     db.session.add(user)
#     db.session.commit()
#
#     return jsonify({
#         "message": f"{user.name}님 회원가입을 축하드립니다",
#         "user_id": user.id
#     }), 201
from flask import Blueprint, request, jsonify
from app.models import User, db
from app.models import AgeStatus, GenderStatus  # Enum 정의된 곳에 따라 경로 조정 필요

users_blp = Blueprint('users', __name__)

# 나이 숫자를 AgeStatus Enum으로 변환하는 함수
def convert_age_to_enum(age):
    if 10 <= age < 20:
        return AgeStatus.teen
    elif 20 <= age < 30:
        return AgeStatus.twenty
    elif 30 <= age < 40:
        return AgeStatus.thirty
    elif 40 <= age < 50:
        return AgeStatus.forty
    else:
        return AgeStatus.fifty

@users_blp.route('/', methods=['GET'])
def connect():
    return jsonify({"message": "Success Connect"})

@users_blp.route('/signup', methods=['POST'])
def signup_page():
    data = request.get_json()

    # 필수 항목 확인
    required_fields = ['name', 'email', 'age', 'gender']
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

    # 👉 여기서 Enum 변환 처리!
    try:
        age_enum = convert_age_to_enum(int(data['age']))
        gender_enum = GenderStatus(data['gender'])  # 예: "male" → GenderStatus.MALE
    except (ValueError, KeyError):
        return jsonify({"message": "잘못된 age 또는 gender 값입니다"}), 400

    # 회원 생성
    user = User(
        name=data['name'],
        email=data['email'],
        age=age_enum,
        gender=gender_enum,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": f"{user.name}님 회원가입을 축하드립니다",
        "user_id": user.id
    }), 201


