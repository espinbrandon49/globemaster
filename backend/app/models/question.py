from app import db
from sqlalchemy import Enum as SAEnum
from app.categories import CategoryKey


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(50))
    category = db.Column(
        SAEnum(CategoryKey, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    
    game_sessions = db.relationship("GameSessionQuestion", back_populates="question")
