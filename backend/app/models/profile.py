from app import db

class Profile(db.Model):
    __tablename__ = "profiles"

    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), primary_key=True)
    avatar = db.Column(db.String(200))
    preferred_difficulty = db.Column(db.String(50))

    player = db.relationship("Player", back_populates="profile")
