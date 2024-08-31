from datetime import timedelta

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

class Database:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()

class Session:
    PERMANENT_SESSION_LIFETIME = timedelta(weeks=1)
    SESSION_PERMANENT = False

class Cookies:
    REMEMBER_COOKIE_DURATION = timedelta(weeks=1)
    REMEMBER_COOKIE_SECURE = True  # Кука передается только по HTTPS
    REMEMBER_COOKIE_HTTPONLY = True  # Кука недоступна через JavaScript
    REMEMBER_COOKIE_SAMESITE = 'Lax'  # Защита от CSRF атак