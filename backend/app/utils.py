from app.models import PlayerBadge, db


def grant_badge_once(player_id, badge_name):
    from app.models import Badge  # local import if needed to avoid circular issues

    badge = Badge.query.filter_by(name=badge_name).first()
    if not badge:
        print(f"⚠️ No badge found with name: {badge_name}")
        return

    already_awarded = PlayerBadge.query.filter_by(
        player_id=player_id, badge_id=badge.id
    ).first()
    if already_awarded:
        print(f"⛔ Badge '{badge_name}' already awarded to player {player_id}")
        return

    db.session.add(PlayerBadge(player_id=player_id, badge_id=badge.id))
    db.session.commit()
    print(f"🏅 Badge '{badge_name}' granted to player {player_id}")
