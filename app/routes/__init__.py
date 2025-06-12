from flask import Blueprint

from .users import bp as users_bp
from .questions import bp as questions_bp
from .choices import bp as choices_bp
from .answers import bp as answers_bp
from .images import bp as images_bp
from .stats_routes import bp as stats_bp  # 제공 파일

bp = Blueprint('routes', __name__)

# 각 Blueprint 등록
bp.register_blueprint(users_bp, url_prefix="/users")
bp.register_blueprint(choices_bp, url_prefix="/choices")
bp.register_blueprint(questions_bp, url_prefix="/questions")
bp.register_blueprint(images_bp, url_prefix="/images")
bp.register_blueprint(answers_bp, url_prefix="/answers")
bp.register_blueprint(stats_bp, url_prefix="/stats")
