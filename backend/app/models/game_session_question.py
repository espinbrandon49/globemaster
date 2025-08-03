from app import db


class GameSessionQuestion(db.Model):
    __tablename__ = "game_session_questions"

    session_id = db.Column(
        db.Integer, db.ForeignKey("game_sessions.id"), primary_key=True
    )
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), primary_key=True)
    player_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)

    session = db.relationship("GameSession", back_populates="questions")
    question = db.relationship("Question", back_populates="game_sessions")
