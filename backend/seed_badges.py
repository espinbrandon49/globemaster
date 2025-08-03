from app import create_app, db
from app.models import Badge

app = create_app()
app.app_context().push()


badges = [
    {
        "name": "Perfect Score",
        "icon": "🎯",
        "description": "Answer all 10 questions correctly in a single session",
    },
    {
        "name": "First Launch",
        "icon": "🚀",
        "description": "Complete your very first game session",
    },
    {
        "name": "Persistent Player",
        "icon": "🔁",
        "description": "Complete 5 total game sessions",
    },
    {
        "name": "Hard Mode Activated",
        "icon": "🧠",
        "description": "Complete a session on Hard difficulty",
    },
    {
        "name": "Perfect Capitals",
        "icon": "🏛️",
        "description": "Answer all Capitals questions correctly in a session",
    },
    {
        "name": "Perfect Landmarks",
        "icon": "🗿",
        "description": "Ace every Famous Landmarks question",
    },
    {
        "name": "Perfect Flags",
        "icon": "🚩",
        "description": "Score 100% in Country Flags questions",
    },
    {
        "name": "Perfect Oceans & Seas",
        "icon": "🌊",
        "description": "Conquer all Oceans and Seas questions",
    },
    {
        "name": "Perfect Cultural Foods",
        "icon": "🍱",
        "description": "Score perfectly in Cultural Foods",
    },
    {
        "name": "Perfect Animal Habitats",
        "icon": "🦁",
        "description": "Get all Animal Habitats answers right",
    },
    {
        "name": "Perfect Languages of the World",
        "icon": "🗣️",
        "description": "Answer all Languages of the World questions correctly",
    },
    {
        "name": "Perfect Natural Wonders",
        "icon": "🏔️",
        "description": "Score 100% on Natural Wonders",
    },
]

for badge_data in badges:
    exists = Badge.query.filter_by(name=badge_data["name"]).first()
    if not exists:
        new_badge = Badge(**badge_data)
        db.session.add(new_badge)
        print(f"✅ Added badge: {badge_data['name']}")
    else:
        print(f"⚠️ Already exists: {badge_data['name']}")

db.session.commit()
print("🏁 Badge seeding complete.")
