from flask import Blueprint, jsonify, request
from app.models import db, Badge, PlayerBadge

badge_bp = Blueprint("badge_bp", __name__)


@badge_bp.route("", methods=["GET"])
def get_all_badges():
    return jsonify(
        [
            {"id": b.id, "name": b.name, "description": b.description, "icon": b.icon}
            for b in Badge.query.all()
        ]
    )


@badge_bp.route("/player/<int:player_id>", methods=["GET"])
def get_player_badges(player_id):
    pb = PlayerBadge.query.filter_by(player_id=player_id).all()
    return jsonify([{"badge_id": b.badge_id, "earned_at": b.earned_at} for b in pb])


@badge_bp.route("/grant", methods=["POST"])
def grant_badge():
    data = request.get_json()
    player_id = data["player_id"]
    badge_id = data["badge_id"]

    existing = PlayerBadge.query.get((player_id, badge_id))
    if existing:
        return jsonify({"message": "Badge already granted"}), 200

    new_entry = PlayerBadge(player_id=player_id, badge_id=badge_id)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Badge granted!"}), 201

