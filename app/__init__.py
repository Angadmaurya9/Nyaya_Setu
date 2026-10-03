"""
NyayaSetu — Application Factory (app/__init__.py)
==================================================
Uses the Flask Application Factory pattern so that the app can be created
with different configurations (development, testing, production) without
restarting the interpreter.

Key extensions initialised here:
  - SQLAlchemy (db)  — ORM / database layer
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config

# Create the SQLAlchemy extension instance.
# It is not bound to an app yet — that happens inside create_app().
db = SQLAlchemy()


def create_app(config_class=None):
    """
    Application factory function.

    Parameters
    ----------
    config_class : class, optional
        A config class from config.py.  If omitted, get_config() is used
        to select the class based on the FLASK_ENV environment variable.

    Returns
    -------
    Flask
        A fully configured Flask application instance.
    """
    app = Flask(
        __name__,
        # Templates folder (Jinja2 looks here automatically)
        template_folder="templates",
        # Static files folder
        static_folder="static",
    )

    # ------------------------------------------------------------------ #
    # Load configuration
    # ------------------------------------------------------------------ #
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # ------------------------------------------------------------------ #
    # Initialise extensions
    # ------------------------------------------------------------------ #
    db.init_app(app)

    # ------------------------------------------------------------------ #
    # Register Blueprints (route modules)
    # ------------------------------------------------------------------ #
    from app.routes.main import main_bp
    from app.routes.legal import legal_bp
    from app.routes.contact import contact_bp

    app.register_blueprint(main_bp)           # /  and general pages
    app.register_blueprint(legal_bp)          # /legal/...
    app.register_blueprint(contact_bp)        # /contact

    # ------------------------------------------------------------------ #
    # Register custom Jinja2 template filters / globals
    # ------------------------------------------------------------------ #
    from app.utils import register_template_helpers
    register_template_helpers(app)

    # ------------------------------------------------------------------ #
    # Create database tables (if they don't already exist)
    # ------------------------------------------------------------------ #
    with app.app_context():
        # Import models so SQLAlchemy knows about them before create_all()
        from app import models  # noqa: F401
        db.create_all()

    return app
