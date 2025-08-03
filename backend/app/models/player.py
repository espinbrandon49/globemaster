from app import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    profile = db.relationship(
        "Profile", back_populates="player", uselist=False, cascade="all, delete-orphan"
    )
    game_sessions = db.relationship(
        "GameSession", back_populates="player", cascade="all, delete-orphan"
    )
    badges = db.relationship(
        "PlayerBadge", backref="player", lazy="dynamic", cascade="all, delete-orphan"
    )
