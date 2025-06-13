# app/routes/choices.py
from flask import Blueprint, request, jsonify
from app.models import db, Choices, Question  # 모델 임포트
from sqlalchemy.orm import joinedload

# Blueprint 정의: url_prefix는 __init__.py에서 처리
choices_blp = Blueprint('choices', __name__) # url_prefix 제거됨

# [예시] 특정 question_id에 해당하는 choice 목록 + 이미지 포함
@choices_blp.route('/question/<int:question_sqe>', methods=['GET'])
def get_choices_by_question(question_sqe):
    question = Question.query.filter_by(id=question_sqe, is_active=True).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    choice_list = (
        Choices.query.filter_by(question_id=question.id, is_active=True)
        .order_by(Choices.sqe)
        .all()
    )
    return jsonify({
        'question': question.title, # 질문 텍스트
        'image': question.image_id, # 질문 이미지 URL
        'choices': [choice.to_dict() for choice in choice_list]
        }
    )

# 1. 모든 선택지 조회 (GET /choices/)
@choices_blp.route('/', methods=['GET'])
def get_all_choices():
    choices = Choices.query.all()
    return jsonify([choice.to_dict() for choice in choices])

# 2. 특정 선택지 상세 조회 (GET /choices/<int:choice_id>)
@choices_blp.route('/<int:choice_id>', methods=['GET'])
def get_choice_detail(choice_id):
    choice = Choices.query.get_or_404(choice_id)
    return jsonify(choice.to_dict())

# 3. 새로운 선택지 생성 (POST /choices/)
@choices_blp.route('/', methods=['POST'])
def create_choice():
    data = request.get_json()

    # 필수 필드: content, question_id, sqe (sqe는 순서)
    if not data or 'content' not in data or 'question_id' not in data or 'sqe' not in data:
        return jsonify({"message": "Missing 'content', 'question_id', or 'sqe' in request body"}), 400

    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({"message": "Question with provided ID not found"}), 404

    try:
        new_choice = Choices(
            content=data['content'], # 'text' 대신 'content'
            question_id=data['question_id'],
            is_active=data.get('is_active', True), # 'is_correct' 대신 'is_active', 기본값 True
            sqe=data['sqe'] # 순서 필드 추가
        )

        db.session.add(new_choice)
        db.session.commit()
        return jsonify(new_choice.to_dict()), 201
    except Exception as e:
        db.session.rollback() # 오류 발생 시 롤백
        return jsonify({"message": f"Error creating choice: {str(e)}"}), 500


# 4. 선택지 업데이트 (PUT /choices/<int:choice_id>)
@choices_blp.route('/<int:choice_id>', methods=['PUT'])
def update_choice(choice_id):
    choice = Choices.query.get_or_404(choice_id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    try:
        if 'content' in data: # 'text' 대신 'content'
            choice.content = data['content']
        if 'is_active' in data: # 'is_correct' 대신 'is_active'
            choice.is_active = data['is_active']
        if 'sqe' in data: # 'sqe' 필드 업데이트
            choice.sqe = data['sqe']
        if 'question_id' in data:
            question = Question.query.get(data['question_id'])
            if not question:
                return jsonify({"message": "Question with provided ID not found"}), 404
            choice.question_id = data['question_id']

        db.session.commit()
        return jsonify(choice.to_dict())
    except Exception as e:
        db.session.rollback() # 오류 발생 시 롤백
        return jsonify({"message": f"Error updating choice: {str(e)}"}), 500


# 5. 선택지 삭제 (DELETE /choices/<int:choice_id>)
@choices_blp.route('/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    choice = Choices.query.get_or_404(choice_id)
    try:
        db.session.delete(choice)
        db.session.commit()
        return jsonify({"message": "Choice deleted successfully"}), 204 # 204 No Content 응답
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting choice: {str(e)}"}), 500