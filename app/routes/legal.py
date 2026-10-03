"""
NyayaSetu — Legal Blueprint (app/routes/legal.py)
==================================================
Handles informational / legal notice pages:
  GET /legal/disclaimer  → Legal disclaimer
  GET /legal/privacy     → Privacy policy
  GET /legal/terms       → Terms of use

IMPORTANT:
  Content on these pages is general information, NOT legal advice.
  A disclaimer is displayed prominently on every legal page.
"""

from flask import Blueprint, render_template
from app.utils import get_language

legal_bp = Blueprint("legal", __name__, url_prefix="/legal")


@legal_bp.route("/disclaimer")
def disclaimer():
    """Legal disclaimer page — explains the limits of the platform."""
    lang = get_language()
    return render_template("legal/disclaimer.html", lang=lang)


@legal_bp.route("/privacy")
def privacy():
    """Privacy policy page — describes what data is (and is not) collected."""
    lang = get_language()
    return render_template("legal/privacy.html", lang=lang)


@legal_bp.route("/terms")
def terms():
    """Terms of use page."""
    lang = get_language()
    return render_template("legal/terms.html", lang=lang)
