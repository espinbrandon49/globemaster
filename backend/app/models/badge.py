from app import db


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    icon = db.Column(db.String(128))  # Optional: path or emoji
