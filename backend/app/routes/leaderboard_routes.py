from flask import Blueprint, jsonify
from app.models import db, Player, GameSession

leaderboard_bp = Blueprint("leaderboard_bp", __name__)

@leaderboard_bp.route("/top-session-scores", methods=["GET"])
def highest_single_session_scores():
    top_sessions = (
        db.session.query(
            GameSession.id.label("session_id"),
            GameSession.score,
            GameSession.questions_answered,
            GameSession.start_time,
            Player.id.label("player_id"),
            Player.name
        )
        .join(Player, Player.id == GameSession.player_id)
        .order_by(GameSession.score.desc())
        .limit(10)
        .all()
    )

    return jsonify([
        {
            "session_id": s.session_id,
            "score": s.score,
            "questions_answered": s.questions_answered,
            "start_time": s.start_time,
            "player_id": s.player_id,
            "player_name": s.name
        } for s in top_sessions
    ])
