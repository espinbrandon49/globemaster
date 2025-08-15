from app import create_app, db
from app.models import Badge
from app.categories import CategoryKey

app = create_app()
app.app_context().push()

badges = [
    {
        "name": "Perfect Score",
        "icon": "🎯",
        "description": "Answer all 10 questions correctly in a single session",
        "category": None,
        "threshold": 10
    },
    {
        "name": "First Launch",
        "icon": "🚀",
        "description": "Complete your very first game session",
        "category": None,
        "threshold": 1
    },
    {
        "name": "Persistent Player",
        "icon": "🔁",
        "description": "Complete 3 total game sessions",
        "category": None,
        "threshold": 3
    },
    {
        "name": "Hard Mode Activated",
        "icon": "🧠",
        "description": "Complete a session on Hard difficulty",
        "category": None,
        "threshold": 1
    },
    {
        "name": "Perfect Capitals",
        "icon": "🏛️",
        "description": "Answer all Capitals questions correctly in a session",
        "category": CategoryKey.CAPITAL_CITIES.value,
        "threshold": 10
    },
    {
        "name": "Perfect Landmarks",
        "icon": "🗿",
        "description": "Ace every Famous Landmarks question",
        "category": CategoryKey.FAMOUS_LANDMARKS.value,
        "threshold": 10
    },
    {
        "name": "Perfect Flags",
        "icon": "🚩",
        "description": "Score 100% in Country Flags questions",
        "category": CategoryKey.COUNTRY_FLAGS.value,
        "threshold": 10
    },
    {
        "name": "Perfect Oceans & Seas",
        "icon": "🌊",
        "description": "Conquer all Oceans and Seas questions",
        "category": CategoryKey.OCEANS_SEAS.value,
        "threshold": 10
    },
    {
        "name": "Perfect Cultural Foods",
        "icon": "🍱",
        "description": "Score perfectly in Cultural Foods",
        "category": CategoryKey.CULTURAL_FOODS.value,
        "threshold": 10
    },
    {
        "name": "Perfect Animal Habitats",
        "icon": "🦁",
        "description": "Get all Animal Habitats answers right",
        "category": CategoryKey.ANIMAL_HABITATS.value,
        "threshold": 10
    },
    {
        "name": "Perfect Languages of the World",
        "icon": "🗣️",
        "description": "Answer all Languages of the World questions correctly",
        "category": CategoryKey.LANGUAGES_WORLD.value,
        "threshold": 10
    },
    {
        "name": "Perfect Natural Wonders",
        "icon": "🏔️",
        "description": "Score 100% on Natural Wonders",
        "category": CategoryKey.NATURAL_WONDERS.value,
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
