from app import db


class GameSession(db.Model):
    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    start_time = db.Column(db.DateTime, server_default=db.func.now())
    score = db.Column(db.Integer)
    questions_answered = db.Column(db.Integer)

    player = db.relationship("Player", back_populates="game_sessions")
    questions = db.relationship(
        "GameSessionQuestion", back_populates="session", cascade="all, delete-orphan"
    )
