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
    send_file, flash, current_app
)
from app.utils import get_language

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
            "\n[URGENT: This application concerns the Life and Liberty of a citizen. "
            "In accordance with the proviso to Section 7(1) of the RTI Act, 2005, the requested "
            "information must be provided within 48 hours of receipt.]\n"
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
{info_text_block}
{urgency_clause}
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

    # Basic Validation
    errors = []
    if not applicant_name:
        errors.append("Applicant name is required." if lang == "en" else "आवेदक का नाम आवश्यक है।")
    if not applicant_address:
        errors.append("Address for correspondence is required." if lang == "en" else "पत्राचार का पता आवश्यक है।")
    if not public_authority:
        errors.append("Public authority / Department name is required." if lang == "en" else "सार्वजनिक प्राधिकरण / विभाग का नाम आवश्यक है।")
    if not subject:
        errors.append("Subject of RTI is required." if lang == "en" else "आरटीआई का विषय आवश्यक है।")
    if not info_requested:
        errors.append("Information requested is required." if lang == "en" else "वांछित सूचना का विवरण आवश्यक है।")

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
        "phone": request.form.get("phone", "").strip(),
        "email": request.form.get("email", "").strip(),
        "public_authority": public_authority,
        "pio_designation": request.form.get("pio_designation", "").strip() or "The Public Information Officer (PIO)",
        "department_address": request.form.get("department_address", "").strip(),
        "subject": subject,
        "info_requested": info_requested,
        "life_liberty": request.form.get("life_liberty", "no"),
        "fee_mode": request.form.get("fee_mode", "ipo"),
        "fee_details": request.form.get("fee_details", "").strip(),
        "bpl_card_no": request.form.get("bpl_card_no", "").strip(),
        "delivery_mode": request.form.get("delivery_mode", "Speed Post").strip(),
        "date": request.form.get("date", "").strip() or datetime.now().strftime("%d/%m/%Y"),
        "place": request.form.get("place", "").strip(),
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
    """
    draft_text = request.form.get("draft_text", "").strip()
    applicant_name = request.form.get("applicant_name", "Applicant").strip()

    if not draft_text:
        flash("Cannot generate PDF from empty text.", "error")
        return redirect(url_for("rti.generator"))

    buffer = io.BytesIO()
    # 0.75 inch margins for standard official documentation
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
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

    # Title
    story.append(Paragraph("APPLICATION FOR SEEKING INFORMATION UNDER THE RIGHT TO INFORMATION ACT, 2005", title_style))
    story.append(Paragraph("<b>[Under Section 6(1) of the RTI Act, 2005]</b>", ParagraphStyle("SubTitle", parent=title_style, fontSize=10, leading=12, spaceAfter=10)))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=12))

    # Convert draft lines to styled paragraphs
    # We preserve paragraph blocks
    paragraphs_raw = draft_text.split("\n\n")

    # If first paragraph has "FORM OF APPLICATION...", we skip or use as subheader
    for block in paragraphs_raw:
        clean_block = block.strip()
        if not clean_block:
            continue

        # Skip duplicate title header if already in raw text
        if "FORM OF APPLICATION FOR SEEKING INFORMATION" in clean_block:
            continue

        # Format line breaks within block
        formatted_html = clean_block.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")

        # Bold labels if starting with numbered sections
        if formatted_html.startswith("1.") or formatted_html.startswith("2.") or formatted_html.startswith("3.") or formatted_html.startswith("4.") or formatted_html.startswith("5."):
            p = Paragraph(f"<b>{formatted_html[:3]}</b>{formatted_html[3:]}", body_style)
        else:
            p = Paragraph(formatted_html, body_style)

        story.append(p)
        story.append(Spacer(1, 4))

    # Trailing line & footer disclaimer
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.gray, spaceAfter=8))
    story.append(Paragraph("Generated via NyayaSetu Citizen Rights Portal — Please verify all particulars and attach ₹10 statutory fee before submitting.", footer_note_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)

    safe_name = "".join(c for c in applicant_name if c.isalnum() or c in (" ", "_")).rstrip()
    safe_name = safe_name.replace(" ", "_") or "Applicant"
    filename = f"RTI_Application_{safe_name}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )
