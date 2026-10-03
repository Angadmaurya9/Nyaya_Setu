"""
NyayaSetu — Application Entry Point (run.py)
=============================================
Start the Flask development server with:
    python run.py

For production, use a WSGI server (e.g., Gunicorn) pointing at the
'app' object in wsgi.py instead of running this script directly.
"""

from app import create_app

# Create the application using config selected by FLASK_ENV variable.
app = create_app()

if __name__ == "__main__":
    # host="0.0.0.0" makes the server accessible on the local network.
    # Debug mode is controlled by the config class (DevelopmentConfig sets it True).
    app.run(host="0.0.0.0", port=5000)
