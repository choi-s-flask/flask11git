from flask import jsonify, request
from flask_smorest import Blueprint

from app.models import Answer
from config import db

answers_blp = Blueprint('answers', __name__, url_prefix='/answers')

@answers_blp.route('', methods=['POST'])
def create_answer():
    data = request.get_json()

    # 필수 데이터 체크 (user_id, choice_id)
    user_id = data.get('user_id')
    choice_id = data.get('choice_id')

    if not user_id or not choice_id:
        return jsonify({"error": "user_id와 choice_id가 필요합니다."}), 400

    # Answer 객체 생성 후 DB에 저장
    answer = Answer(user_id=user_id, choice_id=choice_id)
    db.session.add(answer)
    db.session.commit()

    return jsonify({"message": "답변이 저장되었습니다."}), 201


@answers_blp.route('/<int:user_id>', methods=['GET'])
def get_answers(user_id):
    answers = Answer.query.filter_by(user_id=user_id).all()
    results = []

    for answer in answers:
        results.append({
            "answer_id": answer.id,
            "choice_id": answer.choice_id,
        })

    return jsonify(results), 200