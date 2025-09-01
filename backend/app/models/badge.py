from app import db
from sqlalchemy import Enum as SAEnum
from app.categories import CategoryKey

class Badge(db.Model):
    __tablename__ = "badge"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    icon = db.Column(db.String(128))  # Optional: path or emoji
    category = db.Column(
        SAEnum(CategoryKey, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=True,
    )
    threshold = db.Column(db.Integer, default=10)
