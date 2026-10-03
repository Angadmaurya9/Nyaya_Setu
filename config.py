"""
NyayaSetu — Application Configuration
======================================
Loads settings from environment variables via python-dotenv.
Three configurations are provided:
  - DevelopmentConfig  (default for local development)
  - ProductionConfig   (for deployment)
  - TestingConfig      (for automated tests)

Usage:
    from config import get_config
    app.config.from_object(get_config())
"""

import os
from dotenv import load_dotenv

# Load variables from .env file (if present) into os.environ.
# This call is safe to make even if .env doesn't exist.
load_dotenv()


class BaseConfig:
    """Settings shared across all environments."""

    # Secret key for session signing. MUST be set via environment variable.
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # SQLAlchemy database URI. Defaults to a local SQLite file.
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///nyayasetu.db"
    )
    # Disable SQLAlchemy modification tracking (saves memory).
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Application metadata used in templates.
    APP_NAME: str = "NyayaSetu"
    APP_TAGLINE_EN: str = "Bridging Citizens and Justice"
    APP_TAGLINE_HI: str = "नागरिकों और न्याय के बीच सेतु"

    # Supported languages: (code, label) pairs.
    SUPPORTED_LANGUAGES: list = [("en", "English"), ("hi", "हिन्दी")]
    DEFAULT_LANGUAGE: str = "en"

    # Maximum characters allowed in the issue description textarea.
    ISSUE_MAX_CHARS: int = 1000


class DevelopmentConfig(BaseConfig):
    """Development-specific settings."""
    DEBUG: bool = True
    TESTING: bool = False
    ENV: str = "development"


class ProductionConfig(BaseConfig):
    """Production-specific settings. Debug MUST be off."""
    DEBUG: bool = False
    TESTING: bool = False
    ENV: str = "production"

    def __init__(self):
        # Warn loudly if the default secret key is used in production.
        if self.SECRET_KEY == "dev-secret-change-me":
            import warnings
            warnings.warn(
                "SECRET_KEY is using the insecure default value in production!",
                RuntimeWarning,
                stacklevel=2,
            )


class TestingConfig(BaseConfig):
    """Settings for automated tests."""
    DEBUG: bool = True
    TESTING: bool = True
    ENV: str = "testing"
    # Use an in-memory database so tests never touch the real DB.
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


# Map environment name strings to config classes.
_CONFIG_MAP: dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    """
    Return the appropriate config class based on the FLASK_ENV variable.
    Defaults to DevelopmentConfig if FLASK_ENV is not set or unrecognised.
    """
    env = os.environ.get("FLASK_ENV", "development").lower()
    return _CONFIG_MAP.get(env, DevelopmentConfig)
