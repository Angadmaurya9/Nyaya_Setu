"""
NyayaSetu — Contact Blueprint (app/routes/contact.py)
======================================================
Handles the contact form page:
  GET  /contact  → Display the contact form
  POST /contact  → Process form submission (Phase 1: validates only, no DB write)

Phase 2 will store sanitised contact messages in the ContactMessage model.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.utils import get_language, validate_contact_name, validate_email

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Contact page.

    GET  → Show the form.
    POST → Validate inputs; in Phase 1 just flash success/error.
           No data is stored or emailed in Phase 1.
    """
    lang = get_language()
    form_data = {}      # Repopulate form on validation error
    errors = {}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        # We deliberately do NOT store or process the message body
        # beyond basic validation — this protects user privacy.
        message = request.form.get("message", "").strip()

        # --- Validation ---
        name_ok, name_err = validate_contact_name(name)
        email_ok, email_err = validate_email(email)

        if not name_ok:
            errors["name"] = name_err
        if not email_ok:
            errors["email"] = email_err
        if not subject.strip():
            errors["subject"] = "Subject cannot be empty."
        if not message.strip():
            errors["message"] = "Message cannot be empty."
        if len(message) > 2000:
            errors["message"] = "Message must be at most 2000 characters."

        # Repopulate form so user doesn't have to retype everything.
        form_data = {"name": name, "email": email, "subject": subject}

        if not errors:
            # Phase 1: Acknowledge receipt only. No DB write, no email.
            # TODO (Phase 2): Store ContactMessage and/or send notification email.
            flash(
                "Thank you for reaching out! We will review your message." if lang == "en"
                else "संपर्क करने के लिए धन्यवाद! हम आपके संदेश की समीक्षा करेंगे।",
                "success",
            )
            return redirect(url_for("contact.contact"))

    return render_template(
        "main/contact.html",
        lang=lang,
        form_data=form_data,
        errors=errors,
    )
