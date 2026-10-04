"""
NyayaSetu — RTI Application Generator Blueprint (app/routes/rti.py)
==================================================================
Provides tools to draft, preview, edit, print, and export statutory
Right to Information (RTI) applications under Section 6(1) of the
Right to Information Act, 2005.

Features:
  - GET  /rti            → RTI Application Generator input form
  - POST /rti/generate   → Processes form & renders editable preview
  - POST /rti/export-pdf → Generates compliant A4 PDF via ReportLab
"""

import io
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    send_file, flash, current_app, jsonify
)
from app.utils import get_language
from app.services.gemini_service import generate_rti_questions

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

rti_bp = Blueprint("rti", __name__, url_prefix="/rti")


def build_rti_text(data: dict) -> str:
    """
    Constructs a formal, standard statutory RTI application text
    grounded in Section 6(1) of the Right to Information Act, 2005.
    """
    applicant_name = data.get("applicant_name", "").strip()
    applicant_address = data.get("applicant_address", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()

    public_authority = data.get("public_authority", "").strip()
    pio_designation = data.get("pio_designation", "The Public Information Officer (PIO)").strip()
    department_address = data.get("department_address", "").strip()

    subject = data.get("subject", "").strip()
    info_points = data.get("info_requested", "").strip()
    life_or_liberty = data.get("life_liberty") == "yes"

    fee_mode = data.get("fee_mode", "ipo")
    fee_details = data.get("fee_details", "").strip()
    bpl_card_no = data.get("bpl_card_no", "").strip()

    delivery_mode = data.get("delivery_mode", "Speed Post").strip()
    date_val = data.get("date", datetime.now().strftime("%d/%m/%Y")).strip()
    place_val = data.get("place", "").strip()

    # Format numbered queries
    formatted_points = []
    lines = [l.strip() for l in info_points.split("\n") if l.strip()]
    for idx, line in enumerate(lines, 1):
        # Avoid duplicate numbering if user already entered "1." or "1)"
        cleaned = line
        if line.startswith(f"{idx}.") or line.startswith(f"{idx})"):
            cleaned = line.split(".", 1)[-1].strip() if "." in line else line.split(")", 1)[-1].strip()
        formatted_points.append(f"{idx}. {cleaned}")
    info_text_block = "\n".join(formatted_points) if formatted_points else "1. " + info_points

    # Fee text
    if fee_mode == "bpl":
        fee_clause = (
            f"The applicant belongs to the Below Poverty Line (BPL) category. "
            f"In terms of Section 7(5) of the RTI Act, 2005, no application fee is payable. "
            f"(Copy of BPL Card No. {bpl_card_no or '[Mentioned/Attached]'} is enclosed herewith)."
        )
    elif fee_mode == "ipo":
        fee_clause = (
            f"Application fee of ₹10/- (Rupees Ten only) is paid through Indian Postal Order (IPO) "
            f"No. {fee_details or '[Number]'} dated {date_val}, payable to the Accounts Officer of the public authority."
        )
    elif fee_mode == "dd":
        fee_clause = (
            f"Application fee of ₹10/- (Rupees Ten only) is paid through Demand Draft / Banker's Cheque "
            f"No. {fee_details or '[Number]'} drawn in favour of the Accounts Officer."
        )
    elif fee_mode == "court_fee":
        fee_clause = (
            "Application fee of ₹10/- (Rupees Ten only) is affixed as Court Fee Stamp on this application."
        )
    else:
        fee_clause = (
            f"Application fee of ₹10/- (Rupees Ten only) paid via {fee_details or 'Prescribed Mode'}."
        )

    # Life or liberty note
    urgency_clause = ""
    if life_or_liberty:
        urgency_clause = (
            "\n\n[URGENT: This application concerns the Life and Liberty of a citizen. "
            "In accordance with the proviso to Section 7(1) of the RTI Act, 2005, the requested "
            "information must be provided within 48 hours of receipt.]"
        )

    draft = f"""FORM OF APPLICATION FOR SEEKING INFORMATION UNDER SECTION 6(1)
OF THE RIGHT TO INFORMATION ACT, 2005

To,
{pio_designation},
{public_authority},
{department_address}

1. Full Name of the Applicant: {applicant_name}

2. Address for Correspondence:
   {applicant_address}
   Phone / Mobile: {phone or 'N/A'}
   Email Address: {email or 'N/A'}

3. Particulars of Information Sought:
   (a) Subject of Information: {subject}
   (b) Detailed Particulars of Information Requested:
{info_text_block}{urgency_clause}

   (c) Period to which the information relates: As specified in the points above
   (d) Preferred mode of receiving information: By {delivery_mode}

4. Statutory Declarations:
   (a) I am a citizen of India as required under Section 3 of the Right to Information Act, 2005.
   (b) The information sought does not fall under any of the exemptions contained in Section 8 or Section 9 of the RTI Act, 2005.
   (c) To the best of my knowledge, the information pertains to your office/public authority.

5. Application Fee Details:
   {fee_clause}

Place: {place_val or '[Place]'}
Date: {date_val}

Yours faithfully,


____________________________________
Signature / Thumb Impression of Applicant
({applicant_name})
"""
    return draft.strip()


@rti_bp.route("/")
def generator():
    """RTI Generator Form — collects details to create a formal RTI draft."""
    lang = get_language()
    today_str = datetime.now().strftime("%d/%m/%Y")
    return render_template("rti/generator.html", lang=lang, today=today_str)


@rti_bp.route("/generate", methods=["POST"])
def generate():
    """Processes input and renders the editable draft preview."""
    lang = get_language()

    applicant_name = request.form.get("applicant_name", "").strip()
    applicant_address = request.form.get("applicant_address", "").strip()
    public_authority = request.form.get("public_authority", "").strip()
    subject = request.form.get("subject", "").strip()
    info_requested = request.form.get("info_requested", "").strip()

    # Basic and length validations
    errors = []
    if not applicant_name:
        errors.append("Applicant name is required." if lang == "en" else "आवेदक का नाम आवश्यक है।")
    elif len(applicant_name) > 150:
        errors.append("Applicant name cannot exceed 150 characters.")

    if not applicant_address:
        errors.append("Address for correspondence is required." if lang == "en" else "पत्राचार का पता आवश्यक है।")
    elif len(applicant_address) > 1000:
        errors.append("Address cannot exceed 1000 characters.")

    if not public_authority:
        errors.append("Public authority / Department name is required." if lang == "en" else "सार्वजनिक प्राधिकरण / विभाग का नाम आवश्यक है।")
    elif len(public_authority) > 250:
        errors.append("Public authority name cannot exceed 250 characters.")

    if not subject:
        errors.append("Subject of RTI is required." if lang == "en" else "आरटीआई का विषय आवश्यक है।")
    elif len(subject) > 300:
        errors.append("Subject cannot exceed 300 characters.")

    if not info_requested:
        errors.append("Information requested is required." if lang == "en" else "वांछित सूचना का विवरण आवश्यक है।")
    elif len(info_requested) > 6000:
        errors.append("Information requested cannot exceed 6000 characters.")

    if errors:
        for err in errors:
            flash(err, "error")
        return render_template(
            "rti/generator.html",
            lang=lang,
            form_data=request.form,
            today=datetime.now().strftime("%d/%m/%Y")
        )

    # Form is valid -> generate text
    data_dict = {
        "applicant_name": applicant_name,
        "applicant_address": applicant_address,
        "phone": request.form.get("phone", "").strip()[:30],
        "email": request.form.get("email", "").strip()[:100],
        "public_authority": public_authority,
        "pio_designation": (request.form.get("pio_designation", "").strip() or "The Public Information Officer (PIO)")[:150],
        "department_address": request.form.get("department_address", "").strip()[:500],
        "subject": subject,
        "info_requested": info_requested,
        "life_liberty": request.form.get("life_liberty", "no"),
        "fee_mode": request.form.get("fee_mode", "ipo"),
        "fee_details": request.form.get("fee_details", "").strip()[:100],
        "bpl_card_no": request.form.get("bpl_card_no", "").strip()[:100],
        "delivery_mode": request.form.get("delivery_mode", "Speed Post").strip()[:50],
        "date": (request.form.get("date", "").strip() or datetime.now().strftime("%d/%m/%Y"))[:30],
        "place": request.form.get("place", "").strip()[:100],
    }

    generated_text = build_rti_text(data_dict)

    return render_template(
        "rti/preview.html",
        lang=lang,
        draft_text=generated_text,
        data=data_dict
    )


@rti_bp.route("/export-pdf", methods=["POST"])
def export_pdf():
    """
    Generates a clean, professional, print-ready A4 PDF of the RTI draft using ReportLab.
    Hardened against XML entity parsing errors, malformed markup, line ending variations,
    and memory exhaustion.
    """
    import html
    import re

    draft_text = request.form.get("draft_text", "").strip()
    applicant_name = request.form.get("applicant_name", "Applicant").strip()

    if not draft_text:
        flash("Cannot generate PDF from empty text.", "error")
        return redirect(url_for("rti.generator"))

    # Size ceiling to prevent memory exhaustion / DoS
    if len(draft_text) > 30000:
        flash("Draft text is too large to export to a single PDF document.", "error")
        return redirect(url_for("rti.generator"))

    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "RtiTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=14
        )

        body_style = ParagraphStyle(
            "RtiBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=6
        )

        footer_note_style = ParagraphStyle(
            "RtiFooterNote",
            parent=styles["Italic"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.gray
        )

        story = []

        # Title Block
        story.append(Paragraph("APPLICATION FOR SEEKING INFORMATION UNDER THE RIGHT TO INFORMATION ACT, 2005", title_style))
        story.append(Paragraph("<b>[Under Section 6(1) of the RTI Act, 2005]</b>", ParagraphStyle("SubTitle", parent=title_style, fontSize=10, leading=12, spaceAfter=10)))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=12))

        # 1. Normalize line endings: browsers submit textareas with CRLF (\r\n) per HTML spec
        normalized_text = draft_text.replace("\r\n", "\n").replace("\r", "\n").strip()

        # 2. Strip standard header only from the start of the draft to avoid duplicate Title Block
        header_patterns = [
            r"^\s*FORM OF APPLICATION FOR SEEKING INFORMATION UNDER SECTION 6\(1\)[\s\n]*(OF THE RIGHT TO INFORMATION ACT, 2005)?[\s\n]*",
            r"^\s*APPLICATION FOR SEEKING INFORMATION UNDER THE RIGHT TO INFORMATION ACT, 2005[\s\n]*",
            r"^\s*APPLICATION UNDER SECTION 6\(1\) OF RTI ACT[\s\n]*",
        ]
        clean_text = normalized_text
        for pat in header_patterns:
            clean_text = re.sub(pat, "", clean_text, flags=re.IGNORECASE).strip()

        # 3. Convert draft blocks into styled paragraphs
        paragraphs_raw = re.split(r"\n{2,}", clean_text)

        for block in paragraphs_raw:
            clean_block = block.strip()
            if not clean_block:
                continue

            # Safe HTML escape: prevents XML parsing crashes on '<', '>', '&'
            escaped_text = html.escape(clean_block)
            # Re-introduce line breaks for ReportLab
            formatted_html = escaped_text.replace("\n", "<br/>")

            # Bold standard numbered section heads if present
            if re.match(r"^[1-5]\.", clean_block):
                parts = formatted_html.split(".", 1)
                formatted_html = f"<b>{parts[0]}.</b>{parts[1]}"

            story.append(Paragraph(formatted_html, body_style))
            story.append(Spacer(1, 4))

        # Trailing line & footer disclaimer
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.gray, spaceAfter=8))
        story.append(Paragraph("NyayaSetu is a civic rights and action guidance system for general informational purposes only and does not constitute legal advice. Please verify all particulars and applicable statutory rules before submission.", footer_note_style))

        # Build PDF with graceful error recovery
        doc.build(story)
        buffer.seek(0)

        # Sanitize filename: ASCII alphanumeric characters to guarantee strict RFC & WSGI header compliance
        safe_ascii = "".join(c for c in applicant_name if c.isascii() and (c.isalnum() or c in (" ", "_"))).strip()
        safe_ascii = safe_ascii.replace(" ", "_") or "Applicant"
        filename = f"RTI_Application_{safe_ascii}.pdf"

        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf"
        )

    except Exception as exc:
        current_app.logger.error("ReportLab PDF generation failure: %s", exc)
        flash("PDF generation encountered an error. Please review your text or use the Print button to print/save directly from your browser.", "error")
        return redirect(url_for("rti.generator"))


@rti_bp.route("/suggest-questions", methods=["POST"])
def suggest_questions():
    """
    AI-powered RTI Question Generator API endpoint (Phase 1).
    Accepts JSON or form data:
      - description: str (10 to 1000 characters)
      - lang: str ('en' or 'hi', optional)

    Returns JSON:
      200: {"success": True, "data": {"subject": "...", "questions": [...]}}
      400: {"success": False, "error": "Validation error message"}
      503: {"success": False, "error": "AI service unavailable message"}

    Privacy & Security:
      - Never stores descriptions or generated questions in database, session, or logs.
      - Input validation for string type, empty, min-length (10), and max-length (1000).
    """
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict() if request.form else {}

    description = data.get("description")
    if description is None or not isinstance(description, str):
        return jsonify({
            "success": False,
            "error": "A valid 'description' text is required."
        }), 400

    description_clean = description.strip()
    if not description_clean or len(description_clean) < 10:
        return jsonify({
            "success": False,
            "error": "Please describe your issue or the information needed in at least 10 characters."
        }), 400

    if len(description_clean) > 1000:
        return jsonify({
            "success": False,
            "error": "Description cannot exceed 1000 characters."
        }), 400

    lang = data.get("lang")
    if not lang or not isinstance(lang, str) or lang not in ("en", "hi"):
        lang = get_language() or "en"

    result = generate_rti_questions(description_clean, lang=lang)

    if result.get("success"):
        return jsonify({
            "success": True,
            "data": {
                "subject": result.get("subject", ""),
                "questions": result.get("questions", []),
            }
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": result.get("error") or "AI service is currently unavailable. Please try again later."
        }), 503

