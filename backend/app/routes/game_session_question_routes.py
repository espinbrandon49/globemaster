from flask import Blueprint, request, jsonify
from app.models import GameSessionQuestion, GameSession, Question, db

game_session_question_bp = Blueprint("gsq_bp", __name__)


# GET /game_questions/ — All Answer Entries
@game_session_question_bp.route("/", methods=["GET"])
def get_all_gsq():
    links = GameSessionQuestion.query.all()
    return jsonify(
        [
            {
                "session_id": l.session_id,
                "question_id": l.question_id,
                "player_answer": l.player_answer,
                "is_correct": l.is_correct,
            }
            for l in links
        ]
    )


# POST /game_questions/ — Record Answer to a Question
@game_session_question_bp.route("/", methods=["POST"])
def add_question_to_session():
    data = request.get_json()
    session_id = data.get("session_id")
    question_id = data.get("question_id")
    player_answer = data.get("player_answer")

    session = GameSession.query.get(session_id)
    question = Question.query.get(question_id)

    if not session or not question:
        return jsonify({"error": "Invalid session or question ID"}), 400

    is_correct = (
        player_answer.strip().lower() == question.correct_answer.strip().lower()
    )

    link = GameSessionQuestion(
        session_id=session_id,
        question_id=question_id,
        player_answer=player_answer,
        is_correct=is_correct,
    )
    db.session.add(link)
    
    if is_correct:
        session.score += 1
    
    session.questions_answered += 1
    db.session.commit()

    return jsonify({"message": "Answer recorded", "correct": is_correct}), 201


# DELETE /game_questions/ — Remove a Question from a Session
@game_session_question_bp.route("/", methods=["DELETE"])
def remove_question_from_session():
    data = request.get_json()
    session_id = data.get("session_id")
    question_id = data.get("question_id")

    link = GameSessionQuestion.query.get((session_id, question_id))
    if not link:
        return jsonify({"error": "Entry not found"}), 404

    db.session.delete(link)
    db.session.commit()

    return jsonify({"message": "Question removed from session"})
