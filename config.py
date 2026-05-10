import os

class Config:
    SECRET_KEY = "traveloop-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join("static", "uploads")

    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_SSL_STRICT = False
