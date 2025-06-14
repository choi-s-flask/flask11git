from app.models import Question, Choices, Image
from flask import Blueprint, request, jsonify
from config import db

questions_blp = Blueprint('questions', __name__)

@questions_blp.route('/question', methods=['POST'])
def create_question():

    
        try:
            data = request.get_json()
        
            image = Image.query.get(data.get('image_id'))

            if not image:
                return jsonify({"message": "image not found"}), 404
            
            question = Question(
                title = data['title'],
                sqe = data['sqe'],
                image_id = data['image_id'],
                is_active = data.get('is_active', True),
            )
            db.session.add(question)
            db.session.commit()

            return jsonify({
                "message": f"Title: {question.title} question Success Create"
            }), 201
        except KeyError as e:
            return jsonify({"message": f"Missing required field: {str(e)}"}), 400


@questions_blp.route('/questions/<int:question_sqe>', methods=['GET'])
def get_question(question_sqe):
    question = Question.query.filter_by(sqe=question_sqe, is_active=True).first()

    if not question:
        return jsonify({"error": "존재하지않는 질문입니다" }), 404
    

    choice_list = (Choices.query.filter_by(question_id=question.id, is_active=True).order_by(Choices.sqe)
    .all()
    )
    image = Image.query.get(question.image_id)

    return jsonify({
         "id": question.id,
        "title": question.title,
        "image": image.url if image else None,
        "choices": [choice.to_dict() for choice in choice_list],
    })

    
@questions_blp.route('/questions/count', methods=['GET'])
def get_question_count():
        count = Question.query.filter_by(is_active=True).count()
        return jsonify({"total":count})


