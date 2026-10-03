"""
NyayaSetu — Main Blueprint (app/routes/main.py)
================================================
Handles general pages:
  GET /              → Homepage (index)
  GET /about         → About NyayaSetu
  GET /resources     → Legal resources / useful links
  GET /schemes       → Welfare scheme finder (Phase 1: placeholder)
  GET /issue         → Describe your legal issue (Phase 1: form UI only)
"""

from flask import Blueprint, render_template, current_app
from app.utils import get_language

# Create the Blueprint.
# 'main' is its internal name; url_prefix is '' so routes are at the root.
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage — hero section, feature highlights, quick-access cards."""
    lang = get_language()
    return render_template("main/index.html", lang=lang)


@main_bp.route("/about")
def about():
    """About page — project mission, team, technology stack."""
    lang = get_language()
    return render_template("main/about.html", lang=lang)


@main_bp.route("/resources")
def resources():
    """
    Legal resources page.
    Phase 1: Static list of curated links (helplines, legal-aid sites).
    Phase 2: Will pull from the Resource database model.
    """
    lang = get_language()
    # Static resource data — in Phase 2 this will come from the database.
    resource_list = [
        {
            "title_en": "National Legal Services Authority (NALSA)",
            "title_hi": "राष्ट्रीय विधि सेवा प्राधिकरण (NALSA)",
            "desc_en": "Free legal aid for eligible citizens across India.",
            "desc_hi": "पूरे भारत में पात्र नागरिकों के लिए निःशुल्क कानूनी सहायता।",
            "url": "https://nalsa.gov.in",
            "icon": "⚖️",
        },
        {
            "title_en": "eCourts Services",
            "title_hi": "ई-कोर्ट सेवाएं",
            "desc_en": "Track case status in district and high courts online.",
            "desc_hi": "ऑनलाइन जिला और उच्च न्यायालयों में केस स्थिति ट्रैक करें।",
            "url": "https://ecourts.gov.in",
            "icon": "🏛️",
        },
        {
            "title_en": "India Code — Legislative Portal",
            "title_hi": "इंडिया कोड — विधायी पोर्टल",
            "desc_en": "Full text of all Acts and statutes of India.",
            "desc_hi": "भारत के सभी अधिनियमों और विधियों का पूर्ण पाठ।",
            "url": "https://www.indiacode.nic.in",
            "icon": "📜",
        },
        {
            "title_en": "National Human Rights Commission",
            "title_hi": "राष्ट्रीय मानवाधिकार आयोग",
            "desc_en": "File complaints about human rights violations.",
            "desc_hi": "मानवाधिकार उल्लंघनों के बारे में शिकायत दर्ज करें।",
            "url": "https://nhrc.nic.in",
            "icon": "🛡️",
        },
        {
            "title_en": "Right to Information (RTI) Portal",
            "title_hi": "सूचना का अधिकार (RTI) पोर्टल",
            "desc_en": "File RTI applications with central government bodies.",
            "desc_hi": "केंद्र सरकार के निकायों के साथ RTI आवेदन दाखिल करें।",
            "url": "https://rtionline.gov.in",
            "icon": "📋",
        },
        {
            "title_en": "Consumer Helpline",
            "title_hi": "उपभोक्ता हेल्पलाइन",
            "desc_en": "Register consumer complaints online. National helpline: 1800-11-4000",
            "desc_hi": "ऑनलाइन उपभोक्ता शिकायतें दर्ज करें। राष्ट्रीय हेल्पलाइन: 1800-11-4000",
            "url": "https://consumerhelpline.gov.in",
            "icon": "📞",
        },
    ]
    return render_template("main/resources.html", lang=lang, resources=resource_list)


@main_bp.route("/schemes")
def schemes():
    """
    Welfare scheme finder.
    Phase 1: Informational placeholder page with sample scheme cards.
    Phase 2: Database-backed filterable scheme search with eligibility logic.
    """
    lang = get_language()
    # Sample static schemes — Phase 2 will load these from the Scheme model.
    sample_schemes = [
        {
            "name_en": "Pradhan Mantri Jan Dhan Yojana",
            "name_hi": "प्रधानमंत्री जन धन योजना",
            "desc_en": "Financial inclusion programme providing bank accounts, insurance, and credit.",
            "desc_hi": "बैंक खाते, बीमा और ऋण प्रदान करने वाला वित्तीय समावेशन कार्यक्रम।",
            "category_en": "Financial Inclusion",
            "category_hi": "वित्तीय समावेशन",
            "icon": "🏦",
        },
        {
            "name_en": "PM Awas Yojana (Urban)",
            "name_hi": "प्रधानमंत्री आवास योजना (शहरी)",
            "desc_en": "Housing for all — subsidised home loans for economically weaker sections.",
            "desc_hi": "सभी के लिए आवास — आर्थिक रूप से कमजोर वर्गों के लिए सब्सिडी वाले गृह ऋण।",
            "category_en": "Housing",
            "category_hi": "आवास",
            "icon": "🏠",
        },
        {
            "name_en": "Ayushman Bharat – PM-JAY",
            "name_hi": "आयुष्मान भारत – PM-JAY",
            "desc_en": "Health insurance cover up to ₹5 lakh per family per year.",
            "desc_hi": "प्रति परिवार प्रति वर्ष ₹5 लाख तक का स्वास्थ्य बीमा कवर।",
            "category_en": "Health",
            "category_hi": "स्वास्थ्य",
            "icon": "🏥",
        },
        {
            "name_en": "PM Kisan Samman Nidhi",
            "name_hi": "प्रधानमंत्री किसान सम्मान निधि",
            "desc_en": "Income support of ₹6,000 per year for small and marginal farmers.",
            "desc_hi": "छोटे और सीमांत किसानों के लिए प्रति वर्ष ₹6,000 की आय सहायता।",
            "category_en": "Agriculture",
            "category_hi": "कृषि",
            "icon": "🌾",
        },
    ]
    return render_template("main/schemes.html", lang=lang, schemes=sample_schemes)


@main_bp.route("/issue")
def issue():
    """
    Issue description page.
    Phase 1: Form UI with textarea, character counter, and validation.
    Phase 2: Will connect to AI analysis (Gemini API) and store anonymised queries.
    """
    lang = get_language()
    max_chars = current_app.config.get("ISSUE_MAX_CHARS", 1000)
    return render_template("main/issue.html", lang=lang, max_chars=max_chars)
