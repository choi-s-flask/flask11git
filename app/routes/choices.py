# choices.py
from flask import Blueprint, request, jsonify
from app.models import db, Choice, Question  # 모델 임포트
from sqlalchemy.orm import joinedload

bp = Blueprint('choices', __name__, url_prefix='/choices')

# [예시] 특정 question_id에 해당하는 choice 목록 + 이미지 포함
@bp.route('/question/<int:question_id>', methods=['GET'])
def get_choices_by_question(question_id):
    question = Question.query.options(joinedload(Question.choices)).filter_by(id=question_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    return jsonify({
        'question': question.text,
        'image': question.image_url,
        'choices': [choice.to_dict() for choice in question.choices]
        }
    )

# 1. 모든 선택지 조회 (GET /choices/)
@bp.route('/', methods=['GET'])
def get_all_choices():
    choices = Choice.query.all()
    return jsonify([choice.to_dict() for choice in choices])

# 2. 특정 선택지 상세 조회 (GET /choices/<int:choice_id>)
@bp.route('/<int:choice_id>', methods=['GET'])
def get_choice_detail(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    return jsonify(choice.to_dict())

# 3. 새로운 선택지 생성 (POST /choices/)
@bp.route('/', methods=['POST'])
def create_choice():
    data = request.get_json()

    if not data or 'text' not in data or 'question_id' not in data:
        return jsonify({"message": "Missing 'text' or 'question_id' in request body"}), 400

    question = Question.query.get(data['question_id'])
    if not question:
        return jsonify({"message": "Question with provided ID not found"}), 404

    try:
        new_choice = Choice(
            text=data['text'],
            question_id=data['question_id'],
            is_correct=data.get('is_correct', False)
        )

        db.session.add(new_choice)
        db.session.commit()
        return jsonify(new_choice.to_dict()), 201
    except Exception as e:
        db.session.rollback() # 오류 발생 시 롤백
        return jsonify({"message": f"Error creating choice: {str(e)}"}), 500


# 4. 선택지 업데이트 (PUT /choices/<int:choice_id>)
@bp.route('/<int:choice_id>', methods=['PUT'])
def update_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    try:
        if 'text' in data:
            choice.text = data['text']
        if 'is_correct' in data:
            choice.is_correct = data['is_correct']
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
@bp.route('/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    try:
        db.session.delete(choice)
        db.session.commit()
        return jsonify({"message": "Choice deleted successfully"}), 204 # 204 No Content 응답
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting choice: {str(e)}"}), 500