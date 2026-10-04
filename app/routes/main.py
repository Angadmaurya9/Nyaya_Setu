"""
NyayaSetu — Main Blueprint (app/routes/main.py)
================================================
Handles core civic and guidance routes:
  GET /                  → Homepage (index)
  GET /about             → About NyayaSetu & viva architecture
  GET /resources         → Legal resources & government portal links
  GET, POST /issue       → Problem-to-Action input & classification
  GET /guidance/<slug>   → Verified Action Guidance dashboard for a category
  GET /schemes           → Redirects to issue guidance (schemes discovery out of scope)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.utils import get_language, validate_issue_text
from app.models import LegalCategory, LegalGuidance, Helpline, UserQuery
from app.services.gemini_service import classify_issue, VALID_SLUGS

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage — hero section, problem-to-action flow, verified category list."""
    lang = get_language()
    categories = LegalCategory.query.order_by(LegalCategory.id).all()
    return render_template("main/index.html", lang=lang, categories=categories)


@main_bp.route("/about")
def about():
    """About page — mission, BCA project architecture, privacy-first design."""
    lang = get_language()
    return render_template("main/about.html", lang=lang)


@main_bp.route("/resources")
def resources():
    """
    Curated legal resources and official portal links.
    """
    lang = get_language()
    helplines = Helpline.query.all()
    resource_list = [
        {
            "title_en": "National Legal Services Authority (NALSA)",
            "title_hi": "राष्ट्रीय विधिक सेवा प्राधिकरण (NALSA)",
            "desc_en": "Statutory body providing free, competent legal services to eligible citizens.",
            "desc_hi": "पात्र नागरिकों को निःशुल्क और सक्षम कानूनी सहायता प्रदान करने वाला सांविधिक निकाय।",
            "url": "https://nalsa.gov.in",
            "icon": "⚖️",
        },
        {
            "title_en": "e-Daakhil Consumer Portal",
            "title_hi": "ई-दाखिल उपभोक्ता पोर्टल",
            "desc_en": "Official online consumer dispute filing platform across District, State, and National commissions.",
            "desc_hi": "जिला, राज्य और राष्ट्रीय आयोगों में उपभोक्ता विवाद दर्ज करने हेतु आधिकारिक ऑनलाइन पोर्टल।",
            "url": "https://edaakhil.nic.in",
            "icon": "🛍️",
        },
        {
            "title_en": "National Cyber Crime Reporting Portal",
            "title_hi": "राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल",
            "desc_en": "Ministry of Home Affairs portal for financial cyber fraud and cyber crimes.",
            "desc_hi": "वित्तीय साइबर धोखाधड़ी और साइबर अपराधों के लिए गृह मंत्रालय का आधिकारिक पोर्टल।",
            "url": "https://cybercrime.gov.in",
            "icon": "💻",
        },
        {
            "title_en": "Right to Information (RTI Online)",
            "title_hi": "सूचना का अधिकार (RTI ऑनलाइन)",
            "desc_en": "Official portal to file RTI applications and first appeals for central ministries.",
            "desc_hi": "केंद्रीय मंत्रालयों के लिए आरटीआई आवेदन और प्रथम अपील दाखिल करने का आधिकारिक पोर्टल।",
            "url": "https://rtionline.gov.in",
            "icon": "📋",
        },
        {
            "title_en": "eCourts Services Portal",
            "title_hi": "ई-कोर्ट सेवाएं पोर्टल",
            "desc_en": "Track district and high court case status, cause lists, and certified orders online.",
            "desc_hi": "ऑनलाइन जिला और उच्च न्यायालयों के केस की स्थिति, वाद सूची और आदेश देखें।",
            "url": "https://ecourts.gov.in",
            "icon": "🏛️",
        },
        {
            "title_en": "SAMADHAN Industrial Dispute Portal",
            "title_hi": "समाधान औद्योगिक विवाद पोर्टल",
            "desc_en": "Ministry of Labour portal for conciliation and grievances related to workers and wages.",
            "desc_hi": "श्रमिकों और वेतन से संबंधित सुलह और शिकायतों के लिए श्रम मंत्रालय का पोर्टल।",
            "url": "https://samadhan.labour.gov.in",
            "icon": "💼",
        },
    ]
    return render_template("main/resources.html", lang=lang, resources=resource_list, helplines=helplines)


@main_bp.route("/schemes")
def schemes():
    """
    Scope Correction: Scheme discovery is out of Phase 2 scope.
    Cleanly redirect users to the Issue Guidance flow.
    """
    return redirect(url_for("main.issue"))


@main_bp.route("/issue", methods=["GET", "POST"])
def issue():
    """
    Problem-to-Action entry point.
    GET  → Renders issue description textarea & category selector.
    POST → Runs Gemini classification with keyword fallback,
           records aggregate anonymous query count,
           and renders the verified Guidance Dashboard.
    """
    lang = get_language()
    max_chars = current_app.config.get("ISSUE_MAX_CHARS", 1000)
    categories = LegalCategory.query.order_by(LegalCategory.id).all()

    if request.method == "POST":
        issue_text = request.form.get("issue_text", "").strip()
        manual_category = request.form.get("category", "").strip()

        # Validation
        if not issue_text and not manual_category:
            flash(
                "Please describe your legal issue or select a category." if lang == "en"
                else "कृपया अपनी कानूनी समस्या का विवरण दें या कोई श्रेणी चुनें।",
                "error"
            )
            return render_template("main/issue.html", lang=lang, max_chars=max_chars, categories=categories)

        if issue_text:
            is_valid, err_msg = validate_issue_text(issue_text, max_chars=max_chars)
            if not is_valid:
                flash(err_msg, "error")
                return render_template("main/issue.html", lang=lang, max_chars=max_chars, categories=categories)

        # Classification Logic
        classification_result = {}
        if issue_text:
            classification_result = classify_issue(issue_text)
            matched_slug = classification_result.get("slug", "other")
            method = classification_result.get("method", "keyword")
        elif manual_category in VALID_SLUGS:
            matched_slug = manual_category
            method = "manual"
            classification_result = {"slug": manual_category, "method": "manual", "error": ""}
        else:
            matched_slug = "other"
            method = "fallback"

        # Privacy Protection: NEVER store user issue_text in DB.
        # Only log anonymous aggregate category selection
        try:
            anon_query = UserQuery(
                category_slug=matched_slug,
                classification_method=method,
                language=lang
            )
            db.session.add(anon_query)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return redirect(url_for(
            "main.guidance_dashboard",
            slug=matched_slug,
            method=method
        ))

    return render_template(
        "main/issue.html",
        lang=lang,
        max_chars=max_chars,
        categories=categories
    )


@main_bp.route("/guidance/<slug>")
def guidance_dashboard(slug):
    """
    Verified Guidance Dashboard for a specific legal issue category.
    Displays:
      - Category title and description
      - Numbered, actionable procedural guidance
      - Official statutory sources & hyperlinks
      - Specific departmental helplines
      - Legal disclaimer
    """
    lang = get_language()
    category = LegalCategory.query.filter_by(slug=slug).first()

    if not category:
        category = LegalCategory.query.filter_by(slug="other").first()
        slug = "other"

    guidance_items = []
    if category and category.id:
        guidance_items = LegalGuidance.query.filter_by(
            category_id=category.id,
            verified=True
        ).order_by(LegalGuidance.order_index).all()
    elif not category:
        category = LegalCategory(
            slug="other",
            name_en="General Legal Aid",
            name_hi="सामान्य विधिक सहायता",
            description_en="General citizen rights and free legal assistance under NALSA.",
            description_hi="नालसा के तहत सामान्य नागरिक अधिकार और निःशुल्क कानूनी सहायता।",
            icon="⚖️"
        )

    # Retrieve all helplines and filter relevant ones
    all_helplines = Helpline.query.all()
    relevant_helplines = [h for h in all_helplines if h.is_relevant_to(slug)]

    method = request.args.get("method", "direct")

    return render_template(
        "main/guidance.html",
        lang=lang,
        category=category,
        guidance_items=guidance_items,
        helplines=relevant_helplines,
        method=method
    )
