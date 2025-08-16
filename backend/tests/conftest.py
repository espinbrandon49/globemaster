import os
import sys
import pathlib
import pytest

# Make sure the backend root (which contains the `app/` package) is importable
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

# ✅ Provide a DB URL for tests so config.py doesn't KeyError
# Use a file-backed SQLite DB to avoid in-memory/connection issues on Windows.
os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")

from app import create_app, db  # now safe to import


@pytest.fixture(scope="session")
def app():
    flask_app = create_app()
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    # Build tables once per test session
    with flask_app.app_context():
        db.create_all()
    yield flask_app
    # Teardown: drop tables
    with flask_app.app_context():
        db.drop_all()
