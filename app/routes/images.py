from flask import Flask, jsonify, request, Blueprint
from app.models import Image
from config import db

images_blp = Blueprint('images', __name__, url_prefix='/images')


@images_blp.route("/main", methods=["GET"])
def get_main_image():
    main_image = Image.query.filter_by(type="main").first()

    if not main_image:
        return jsonify({"image": None, "message": "메인 이미지가 없습니다."}), 404

    return jsonify({"image": main_image.url}), 200


@images_blp.route("", methods=["POST"])
def create_image():
    try:
        data = request.get_json()

        # 요청 데이터에서 url과 type 가져오기
        image_url = data.get("url")
        image_type = data.get("type")  # "main" 또는 "sub"

        # 값이 없으면 에러 반환
        if not image_url or not image_type:
            return jsonify({"error": "url과 type은 필수입니다."}), 400

        # 새 이미지 객체 생성 및 DB에 저장
        new_image = Image(url=image_url, type=image_type)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": f"ID: {new_image.id} Image Success Create"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
