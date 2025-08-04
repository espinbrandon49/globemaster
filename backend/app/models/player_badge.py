from app import db


class PlayerBadge(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), primary_key=True)
    earned_at = db.Column(db.DateTime, server_default=db.func.now())
# from app.models import PlayerBadge
# [(pb.badge_id, pb.earned_at) for pb in PlayerBadge.query.filter_by(player_id=18).all()]
