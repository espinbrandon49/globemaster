from flask import Blueprint, request, jsonify
from app.models import GameSession, GameSessionQuestion, Player, Question, Profile, db
import random
from app.utils import grant_badge_once


game_bp = Blueprint("game_bp", __name__)


# GET /games/ — All Game Sessions
@game_bp.route("/", methods=["GET"])
def get_all_game_sessions():
    sessions = GameSession.query.all()
    return jsonify(
        [
            {
                "id": s.id,
                "player_id": s.player_id,
                "start_time": s.start_time,
                "score": s.score,
                "questions_answered": s.questions_answered,
            }
            for s in sessions
        ]
    )


# GET /games/<id> — One Game Session
@game_bp.route("/<int:session_id>", methods=["GET"])
def get_game_session(session_id):
    s = GameSession.query.get(session_id)
    if not s:
        return jsonify({"error": "Game session not found"}), 404

    return jsonify(
        {
            "id": s.id,
            "player_id": s.player_id,
            "start_time": s.start_time,
            "score": s.score,
            "questions_answered": s.questions_answered,
        }
    )


# POST /games/ — Start New Session with Dynamic Question Selection
@game_bp.route("/", methods=["POST"])
def create_game_session():
    data = request.get_json()
    player_id = data.get("player_id")
    category = data.get("category")
    use_difficulty = data.get("use_difficulty", False)

    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    # Create the game session
    session = GameSession(player_id=player_id, score=0, questions_answered=0)
    db.session.add(session)
    db.session.flush()  # gets session.id before commit

    # First Launch → 🚀
    session_count = GameSession.query.filter_by(player_id=player_id).count()
    if session_count == 1:
        grant_badge_once(player_id, "First Launch")

    # Fetch questions
    questions_query = Question.query

    if category:
        questions_query = questions_query.filter_by(category=category)
    elif use_difficulty:
        profile = Profile.query.filter_by(player_id=player_id).first()
        if not profile:
            return jsonify({"error": "Profile not found for player"}), 404
        questions_query = questions_query.filter_by(
            difficulty=profile.preferred_difficulty
        )
    else:
        return (
            jsonify(
                {"error": "Must provide either 'category' or 'use_difficulty': true"}
            ),
            400,
        )

    questions = questions_query.all()
    if not questions:
        return jsonify({"error": "No questions found for the selection"}), 404

    selected = random.sample(questions, min(10, len(questions)))

    db.session.commit()

    # 🔁 Persistent Player — "Complete 5 total game sessions"
    session_total = GameSession.query.filter_by(player_id=player_id).count()
    if session_total == 5:
        grant_badge_once(player_id, "Persistent Player")

    return (
        jsonify(
            {
                "id": session.id,
                "questions": [
                    {
                        "id": q.id,
                        "text": q.text,
                        "category": q.category,
                        "difficulty": q.difficulty,
                        "correct_answer": q.correct_answer,
                    }
                    for q in selected
                ],
            }
        ),
        201,
    )


# PUT /games/<id> — Update Score or Questions Answered
@game_bp.route("/<int:session_id>", methods=["PUT"])
def update_game_session(session_id):
    session = GameSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    data = request.get_json()
    session.score = data.get("score", session.score)
    session.questions_answered = data.get(
        "questions_answered", session.questions_answered
    )

    db.session.commit()

    # Perfect Score → 🎯
    if session.score == 10:
        grant_badge_once(session.player_id, "Perfect Score")

    # 🏷️ Category-Specific Perfect Score Badges
    session_questions = (
        GameSessionQuestion.query.filter_by(session_id=session_id)
        .join(Question, GameSessionQuestion.question_id == Question.id)
        .with_entities(GameSessionQuestion.is_correct, Question.category)
        .all()
    )

    if len(session_questions) == 10 and all(q[0] for q in session_questions):
        categories = {q[1] for q in session_questions}
        if len(categories) == 1:
            category = categories.pop()

            category_badges = {
                "Capitals": "Perfect Capitals",
                "Famous Landmarks": "Perfect Landmarks",
                "Country Flags": "Perfect Flags",
                "Oceans and Seas": "Perfect Oceans & Seas",
                "Cultural Foods": "Perfect Cultural Foods",
                "Animal Habitats": "Perfect Animal Habitats",
                "Languages of the World": "Perfect Languages of the World",
                "Natural Wonders": "Perfect Natural Wonders",
            }
            
            badge_name = category_badges.get(category)
            if badge_name:
                grant_badge_once(session.player_id, badge_name)

    return jsonify({"message": "Session updated"})


# DELETE /games/<id> — Remove GameSession
@game_bp.route("/<int:session_id>", methods=["DELETE"])
def delete_game_session(session_id):
    session = GameSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": "session deleted"})
