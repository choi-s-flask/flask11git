# app/routes/choices.py
from flask import Blueprint, request, jsonify
from app.models import db, Choices, Question  # 모델 임포트
from sqlalchemy.orm import joinedload

# Blueprint 정의: url_prefix는 __init__.py에서 처리
choices_blp = Blueprint('choices', __name__, url_prefix='/choice') # url_prefix 제거됨

@choices_blp.route('', methods=['POST'])
def create_choice():
    data = request.get_json()

    # 필수 필드 확인
    required_fields = ['content', 'question_id', 'sqe']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"message": f"다음 필드가 누락되었습니다: {', '.join(missing)}"}), 400

    # 질문 존재 여부 확인
    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({"message": "해당 question_id에 해당하는 질문이 존재하지 않습니다"}), 404

    try:
        # 선택지 생성
        new_choice = Choices(
            content=data['content'],
            question_id=data['question_id'],
            is_active=data.get('is_active', True),  # 기본값 True
            sqe=data['sqe']
        )

        db.session.add(new_choice)
        db.session.commit()

        return jsonify({
            "message": f"Content: {new_choice.content} choice Success Create"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating choice: {str(e)}"}), 500

