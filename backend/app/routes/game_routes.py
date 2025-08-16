from flask import Blueprint, request, jsonify
from sqlalchemy import func, case
from app.models import GameSession, GameSessionQuestion, Player, Question, Profile, Badge, db
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
        
    if use_difficulty:
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
    session = GameSession.query.get_or_404(session_id)

    # 🔒 Recompute from authoritative answers; ignore any client-provided numbers
    totals = (
        db.session.query(
            func.sum(case((GameSessionQuestion.is_correct == True, 1), else_=0)).label("score"),
            func.count(GameSessionQuestion.question_id).label("answered"),
        )
        .filter(GameSessionQuestion.session_id == session.id)
        .one()
    )
    session.score = int(totals.score or 0)
    session.questions_answered = int(totals.answered or 0)
    db.session.commit()

    # ✅ DEBUG: Print current session state (keep your existing lines below this)
    print(f"🧪 [Badge Check] Session {session.id} — Score: {session.score}, Questions Answered: {session.questions_answered}")

    # 🔥 BADGE: Perfect Score
    if session.score == 10:
        grant_badge_once(session.player_id, "Perfect Score")
        print(f"✅ Checked for Perfect Score badge on session {session.id}")

    # 🔥 BADGE: Category-specific (unchanged)
    results = (
        db.session.query(GameSessionQuestion.is_correct, Question.category)
        .join(Question, GameSessionQuestion.question_id == Question.id)
        .filter(GameSessionQuestion.session_id == session.id)
        .all()
    )
    category_counts = {}
    for is_correct, category in results:
        if is_correct:
            category_counts[category] = category_counts.get(category, 0) + 1

    badges = Badge.query.filter(Badge.category != None).all()
    for badge in badges:
        count = category_counts.get(badge.category, 0)
        if count >= badge.threshold:
            grant_badge_once(session.player_id, badge.name)

    return jsonify({
        "id": session.id,
        "player_id": session.player_id,
        "start_time": session.start_time,
        "score": session.score,
        "questions_answered": session.questions_answered,
    })
