from app import create_app, db
from app.models import Badge

app = create_app()
app.app_context().push()


badges = [
    {
        "name": "Perfect Score",
        "icon": "🎯",
        "description": "Answer all 10 questions correctly in a single session",
        "category": "Score",
        "threshold": 10
    },
    {
        "name": "First Launch",
        "icon": "🚀",
        "description": "Complete your very first game session",
        "category": "First",
        "threshold": 1
    },
    {
        "name": "Persistent Player",
        "icon": "🔁",
        "description": "Complete 3 total game sessions",
        "category": "Persistent",
        "threshold": 3
    },
    {
        "name": "Hard Mode Activated",
        "icon": "🧠",
        "description": "Complete a session on Hard difficulty",
        "category": "Hard",
        "threshold": 1
    },
    {
        "name": "Perfect Capitals",
        "icon": "🏛️",
        "description": "Answer all Capitals questions correctly in a session",
        "category": "Capitals",
        "threshold": 10
    },
    {
        "name": "Perfect Landmarks",
        "icon": "🗿",
        "description": "Ace every Famous Landmarks question",
        "category": "Landmarks",
        "threshold": 10
    },
    {
        "name": "Perfect Flags",
        "icon": "🚩",
        "description": "Score 100% in Country Flags questions",
        "category": "Flags",
        "threshold": 10
    },
    {
        "name": "Perfect Oceans & Seas",
        "icon": "🌊",
        "description": "Conquer all Oceans and Seas questions",
        "category": "Oceans",
        "threshold": 10
    },
    {
        "name": "Perfect Cultural Foods",
        "icon": "🍱",
        "description": "Score perfectly in Cultural Foods",
        "category": "Foods",
        "threshold": 10
    },
    {
        "name": "Perfect Animal Habitats",
        "icon": "🦁",
        "description": "Get all Animal Habitats answers right",
        "category": "Habitats",
        "threshold": 10
    },
    {
        "name": "Perfect Languages of the World",
        "icon": "🗣️",
        "description": "Answer all Languages of the World questions correctly",
        "category": "Languages",
        "threshold": 10
    },
    {
        "name": "Perfect Natural Wonders",
        "icon": "🏔️",
        "description": "Score 100% on Natural Wonders",
        "category": "Wonders",
        "threshold": 10
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
