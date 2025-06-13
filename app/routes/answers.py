from flask import jsonify, request
from flask_smorest import Blueprint

from app.models import Answer
from config import db

answers_blp = Blueprint('answers', __name__)

@answers_blp.route("/submit", methods=["POST"])
def submit_answer():
    try:
        data_list = request.get_json()  # 한 번만 호출

        for data in data_list:
            answer = Answer(
                user_id=data["user_id"],
                choice_id=data["choice_id"],
            )
            db.session.add(answer)

        db.session.commit()
        user_id = data_list[0]["user_id"]

        return jsonify(
            {"message": f"User: {user_id}'s answers successfully created"}
        ), 201

    except KeyError as e:
        return jsonify({"message": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        # 예외 잡아서 디버깅에 도움
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500