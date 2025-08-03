import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]  # Required env var
    SQLALCHEMY_TRACK_MODIFICATIONS = False