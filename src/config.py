import os

DB_USER = os.environ.get("DB_USER", "advert_app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "secret")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "advert_app")

JWT_SECRET = os.environ.get("JWT_SECRET", "secret")
