import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _db_url():
    url = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'portfolio.db')}")
    # Neon / Heroku return postgres:// — SQLAlchemy requires postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://") and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # Re-encode the password so special chars like @ don't break URL parsing.
    # Strategy: the last @ separates userinfo from host; everything before it
    # (after the scheme) is "user:raw_password".
    if "postgresql" in url or "cockroachdb" in url:
        scheme_end = url.index("://") + 3
        scheme = url[:scheme_end]
        rest = url[scheme_end:]
        last_at = rest.rfind("@")
        if last_at != -1:
            userinfo = rest[:last_at]       # "user:raw_password"
            hostpart = rest[last_at + 1:]   # "host:port/db?params"
            colon = userinfo.find(":")
            if colon != -1:
                user = userinfo[:colon]
                raw_password = userinfo[colon + 1:]
                encoded_password = quote(raw_password, safe="")
                url = f"{scheme}{user}:{encoded_password}@{hostpart}"

    # CockroachDB needs its own dialect to parse the version string correctly
    if "cockroachlabs.cloud" in url:
        url = url.replace("postgresql+psycopg2://", "cockroachdb+psycopg2://", 1)
        url = url.replace("postgresql://", "cockroachdb+psycopg2://", 1)

    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production-use-a-strong-random-key")
    SQLALCHEMY_DATABASE_URI = _db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
