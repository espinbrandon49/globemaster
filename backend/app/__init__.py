from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Apply CORS before routes — allow Vite dev server (5173)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Register routes
    from app.routes.player_routes import player_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.question_routes import question_bp
    from app.routes.game_routes import game_bp
    from app.routes.game_session_question_routes import game_session_question_bp
    from app.routes.badge_routes import badge_bp
    from app.routes.leaderboard_routes import leaderboard_bp
    from app.routes.meta_routes import meta_bp

    app.register_blueprint(player_bp, url_prefix="/players")
    app.register_blueprint(profile_bp, url_prefix="/profiles")
    app.register_blueprint(question_bp, url_prefix="/questions")
    app.register_blueprint(game_bp, url_prefix="/games")
    app.register_blueprint(game_session_question_bp, url_prefix="/game_questions")
    app.register_blueprint(badge_bp, url_prefix="/badges")
    app.register_blueprint(leaderboard_bp, url_prefix="/leaderboard")
    app.register_blueprint(meta_bp, url_prefix="/meta")

    return app
