"""
NyayaSetu — Utility / Helper Functions (app/utils.py)
=====================================================
Contains:
  - Template context helpers (language detection, active-page tracking)
  - Input validation helpers
  - Jinja2 filter / global registration

These are kept separate from routes so they can be tested independently
and reused across multiple blueprints.
"""

from flask import request, session
from markupsafe import Markup


# ─────────────────────────────────────────────────────────────────────────────
# Language helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_language() -> str:
    """
    Determine the active language for the current request.

    Priority order:
      1. ?lang= query parameter in the URL
      2. 'lang' key stored in the Flask session
      3. Default to 'en'

    The chosen language is saved to the session so it persists across pages.
    """
    lang = request.args.get("lang") or session.get("lang", "en")
    # Only accept supported language codes to prevent injection.
    if lang not in ("en", "hi"):
        lang = "en"
    session["lang"] = lang
    return lang


# ─────────────────────────────────────────────────────────────────────────────
# Input validation helpers
# ─────────────────────────────────────────────────────────────────────────────

def validate_issue_text(text: str, max_chars: int = 1000) -> tuple[bool, str]:
    """
    Validate text submitted in the issue-description textarea.

    Returns
    -------
    (is_valid: bool, error_message: str)
    """
    if not text or not text.strip():
        return False, "Issue description cannot be empty."
    if len(text) > max_chars:
        return False, f"Issue description must be at most {max_chars} characters."
    return True, ""


def validate_contact_name(name: str) -> tuple[bool, str]:
    """Basic validation for a contact name field."""
    if not name or not name.strip():
        return False, "Name cannot be empty."
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters."
    if len(name) > 100:
        return False, "Name must be at most 100 characters."
    return True, ""


def validate_email(email: str) -> tuple[bool, str]:
    """Rudimentary e-mail format check (no external library needed)."""
    import re
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not email or not email.strip():
        return False, "Email address cannot be empty."
    if not re.match(pattern, email.strip()):
        return False, "Please enter a valid email address."
    return True, ""


# ─────────────────────────────────────────────────────────────────────────────
# Jinja2 registration
# ─────────────────────────────────────────────────────────────────────────────

def register_template_helpers(app) -> None:
    """
    Register custom Jinja2 globals and filters on the Flask app.

    Globals are available in every template without needing to pass them
    from each view function.
    """

    @app.context_processor
    def inject_globals():
        """
        Inject variables available in *every* Jinja2 template:
          - lang          : active language code ('en' or 'hi')
          - app_name      : application name string
          - current_path  : current URL path (for active-nav highlighting)
        """
        return {
            "lang": get_language(),
            "app_name": app.config.get("APP_NAME", "NyayaSetu"),
            "current_path": request.path,
            "issue_max_chars": app.config.get("ISSUE_MAX_CHARS", 1000),
        }

    @app.template_filter("truncate_words")
    def truncate_words_filter(text: str, count: int = 20) -> Markup:
        """
        Jinja2 filter: truncate *text* to *count* words, appending '…'.
        Usage in template: {{ some_text | truncate_words(15) }}
        """
        words = text.split()
        if len(words) <= count:
            return Markup(text)
        return Markup(" ".join(words[:count]) + "…")
