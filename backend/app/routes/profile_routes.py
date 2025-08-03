from flask import Blueprint, request, jsonify
from app.models import Profile, Player, db
from app.utils import grant_badge_once

profile_bp = Blueprint("profile_bp", __name__)


# GET /profiles/ — All Profiles
@profile_bp.route("/", methods=["GET"])
def get_all_profiles():
    profiles = Profile.query.all()
    return jsonify(
        [
            {
                "player_id": p.player_id,
                "avatar": p.avatar,
                "preferred_difficulty": p.preferred_difficulty,
            }
            for p in profiles
        ]
    )


# GET /profiles/<player_id> — Single Player's Profile
@profile_bp.route("/<int:player_id>", methods=["GET"])
def get_profile(player_id):
    profile = Profile.query.get(player_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify(
        {
            "player_id": profile.player_id,
            "avatar": profile.avatar,
            "preferred_difficulty": profile.preferred_difficulty,
        }
    )


# PUT /profiles/<player_id> — Update Profile
@profile_bp.route("/", methods=["POST"])
def create_or_update_profile():
    data = request.get_json()
    player_id = data.get("player_id")
    avatar = data.get("avatar")
    preferred_difficulty = data.get("preferred_difficulty")

    if not player_id or not avatar or not preferred_difficulty:
        return jsonify({"error": "Missing required fields"}), 400
    
    #  Hard Mode Activated → 🧠
    if preferred_difficulty == "Hard":
        grant_badge_once(player_id, "Hard Mode Activated")

    # Check if a profile already exists for this player
    profile = Profile.query.filter_by(player_id=player_id).first()

    if profile:
        # Update existing profile
        profile.avatar = avatar
        profile.preferred_difficulty = preferred_difficulty
    else:
        # Create a new profile
        profile = Profile(
            player_id=player_id,
            avatar=avatar,
            preferred_difficulty=preferred_difficulty,
        )
        db.session.add(profile)

    db.session.commit()

    return (
        jsonify(
            {
                "player_id": profile.player_id,
                "avatar": profile.avatar,
                "preferred_difficulty": profile.preferred_difficulty,
            }
        ),
        200,
    )


# DELETE /profiles/<player_id> — Delete Profile
@profile_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_profile(player_id):
    profile = Profile.query.get(player_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    db.session.delete(profile)
    db.session.commit()
    return jsonify({"message": "Profile deleted"})
