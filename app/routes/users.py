from flask import Blueprint, request, jsonify
from app.models import User, db

user_blp = Blueprint("user", __name__)

@user_blp.route("/signup", methods=["POST"])
def signup_page():
    try:
        data = request.get_json()

        # 필수 필드 검사
        required_fields = ["name", "email", "age", "gender"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            return jsonify({"message": f"Missing required field: {', '.join(missing)}"}), 400

        # 이메일 중복 검사
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"message": "이미 존재하는 계정 입니다."}), 400

        # 회원 생성
        user = User(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            gender=data["gender"]
        )
        db.session.add(user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"{user.name}님 회원가입을 축하합니다",
                    "user_id": user.id
                }
            ),
            201,
        )

    except KeyError as e:
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"서버 오류: {str(e)}"}), 500


