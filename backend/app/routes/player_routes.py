from flask import Blueprint, request, jsonify
from app.models import Player, Profile, db

player_bp = Blueprint("player_bp", __name__)


# GET /players — Fetch All Players
@player_bp.route("/", methods=["GET"])
def get_players():
    players = Player.query.all()
    return jsonify([{"id": p.id, "name": p.name, "email": p.email} for p in players])


# GET /players/<id>
@player_bp.route("/<int:player_id>", methods=["GET"])
def get_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    return jsonify({"id": player.id, "name": player.name, "email": player.email})


# POST /players — Create a New Player
@player_bp.route("/", methods=["POST"])
def create_player():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_player = Player(name=name, email=email)
    db.session.add(new_player)
    db.session.commit()

    return (
        jsonify(
            {"id": new_player.id, "name": new_player.name, "email": new_player.email}
        ),
        201,
    )


# PUT /players/<id>
@player_bp.route("/<int:player_id>", methods=["PUT"])
def update_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    data = request.get_json()
    player.name = data.get("name", player.name)
    player.email = data.get("email", player.email)

    db.session.commit()
    return jsonify({"message": "Player updated successfully"})


# DELETE /players/<id>
@player_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    db.session.delete(player)
    db.session.commit()
    return jsonify({"message": "player deleted"})


# GET /players/email/<email>
@player_bp.route("/email/<path:email>", methods=["GET"])
def get_player_by_email(email):
    player = Player.query.filter_by(email=email).first()
    if player:
        return (
            jsonify({"id": player.id, "name": player.name, "email": player.email}),
            200,
        )
    return jsonify({"error": "Player not found"}), 404
