from flask import Blueprint, request, jsonify
from app.models import Question, db

question_bp = Blueprint("question_bp", __name__)


# GET /questions/ — All Questions
@question_bp.route("", methods=["GET"])
def get_questions():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")

    query = Question.query

    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    questions = query.order_by(db.func.random()).limit(10).all()

    return jsonify(
        [
            {
                "id": q.id,
                "text": q.text,
                "correct_answer": q.correct_answer,
                "category": q.category,
                "difficulty": q.difficulty,
            }
            for q in questions
        ]
    )


# GET /questions/<id> — One Question
@question_bp.route("/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    q = Question.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404

    return jsonify(
        {
            "id": q.id,
            "text": q.text,
            "correct_answer": q.correct_answer,
            "category": q.category,
            "difficulty": q.difficulty,
        }
    )


# POST /questions/ — Create Question
@question_bp.route("/", methods=["POST"])
def create_question():
    data = request.get_json()
    text = data.get("text")
    correct_answer = data.get("correct_answer")
    category = data.get("category")
    difficulty = data.get("difficulty")

    if not text or not correct_answer or not category:
        return (
            jsonify({"error": "Text, correct answer, and category are required"}),
            400,
        )

    q = Question(
        text=text,
        correct_answer=correct_answer,
        category=category,
        difficulty=difficulty,
    )
    db.session.add(q)
    db.session.commit()

    return jsonify({"message": "Question created", "id": q.id}), 201


# PUT /questions/<id> — Update
@question_bp.route("/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    q = Question.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()
    q.text = data.get("text", q.text)
    q.correct_answer = data.get("correct_answer", q.correct_answer)
    q.category = data.get("category", q.category)
    q.difficulty = data.get("difficulty", q.difficulty)

    db.session.commit()
    return jsonify({"message": "Question updated successfully"})


# Delete a player
@question_bp.route("/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    q = Question.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(q)
    db.session.commit()
    return jsonify({"message": "Question deleted"})
