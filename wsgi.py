"""
NyayaSetu — WSGI Entry Point (wsgi.py)
=======================================
Used by production WSGI servers such as Gunicorn:
    gunicorn wsgi:app --workers 4 --bind 0.0.0.0:8000

The FLASK_ENV environment variable should be set to 'production'
on the server so ProductionConfig is loaded automatically.
"""

from app import create_app

app = create_app()
