"""
NyayaSetu — Gemini API Service (app/services/gemini_service.py)
================================================================
Provides issue classification using the Google Gemini API.

How it works:
  1. `classify_issue(text)` is called with the user's plain-language description.
  2. It sends a carefully constrained prompt to Gemini asking it to return
     ONLY one of the recognised category slugs (no free-form legal advice).
  3. If the API key is missing, quota is exceeded, or the network is down,
     it falls back to `keyword_classify(text)` — a simple keyword-matching
     function that covers common cases without any external dependency.

Security:
  - The API key is loaded from the environment variable GEMINI_API_KEY.
  - It is NEVER hardcoded here or logged.
  - The prompt explicitly forbids Gemini from giving legal advice.

Returns:
  dict with keys:
    slug   (str)  — category slug, e.g. "consumer"
    method (str)  — "gemini" | "keyword" | "fallback"
    error  (str)  — empty string if no error
"""

import os
import logging
import re

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Recognised category slugs — MUST match LegalCategory.slug in the database.
# ─────────────────────────────────────────────────────────────────────────────
VALID_SLUGS = {
    "consumer",
    "property",
    "family",
    "labour",
    "rti",
    "criminal",
    "domestic_violence",
    "other",
}

# ─────────────────────────────────────────────────────────────────────────────
# Gemini prompt template
# ─────────────────────────────────────────────────────────────────────────────
_CLASSIFICATION_PROMPT = """You are a legal issue classifier for an Indian legal aid platform called NyayaSetu.

Your ONLY job is to read the user's issue description and return the single most relevant category slug from this list:

consumer          - Consumer complaints, defective goods, service deficiency, e-commerce disputes
property          - Land disputes, tenancy, eviction, property registration, RERA
family            - Divorce, maintenance, dowry, child custody, adoption, inheritance
labour            - Unpaid wages, wrongful termination, workplace harassment, PF/ESI issues
rti               - Right to Information requests, government information denial
criminal          - FIR, bail, criminal complaints, theft, cheating, fraud
domestic_violence - Physical, emotional or financial abuse at home
other             - Does not fit any above category

Rules:
1. Reply with EXACTLY ONE slug from the list above. Nothing else.
2. Do NOT provide any legal advice, explanation or commentary.
3. If the issue is in Hindi, still classify and return only the slug.
4. If truly ambiguous, return: other

User issue description:
\"\"\"
{issue_text}
\"\"\"

Reply with only the slug:"""

# ─────────────────────────────────────────────────────────────────────────────
# Keyword fallback — no external dependencies
# ─────────────────────────────────────────────────────────────────────────────
_KEYWORD_MAP = [
    # (slug, keywords to match — lowercase)
    ("domestic_violence", [
        "domestic violence", "घरेलू हिंसा", "wife beating", "husband beating",
        "abuse at home", "घर में मार", "domestic abuse", "marital violence",
        "घरेलू उत्पीड़न", "torture at home", "harassment by in-laws",
        "ससुराल में प्रताड़ना", "पति द्वारा मारपीट", "शारीरिक प्रताड़ना",
        "protection order", "संरक्षण आदेश", "dv act",
    ]),
    ("rti", [
        "rti", "right to information", "सूचना का अधिकार", "information request",
        "government document", "सरकारी दस्तावेज", "application rejected",
        "pio", "cpio", "spio", "public information officer", "जन सूचना अधिकारी",
        "transparency", "first appeal", "प्रथम अपील", "second appeal",
        "द्वितीय अपील", "cic", "sic", "information commissioner",
        "सूचना आयोग", "सरकारी रिकॉर्ड", "noting sheet", "exam copy",
    ]),
    ("consumer", [
        "consumer", "उपभोक्ता", "defective", "खराब", "refund", "वापसी",
        "पैसे वापस", "product", "service", "e-commerce", "amazon", "flipkart",
        "online shopping", "ऑनलाइन शॉपिंग", "cheating by company", "bill",
        "overcharge", "insurance claim", "बीमा क्लेम", "warranty", "वारंटी",
        "guarantee", "गारंटी", "damaged", "repair", "seller", "विक्रेता",
        "shopkeeper", "दुकानदार", "store", "दुकान", "purchase", "खरीदा",
        "खरीदी", "order", "return", "replacement", "एक्सचेंज", "expiry",
        "expired", "mrp", "एमआरपी", "adulterated", "मिलावट", "deficiency in service",
        "flight cancellation", "ticket refund", "hotel booking", "ग्राहकों",
        "ग्राहक", "उपभोक्ता फोरम",
    ]),
    ("property", [
        "property", "संपत्ति", "land", "जमीन", "plot", "प्लाट", "प्लॉट",
        "rent", "किराया", "tenant", "किरायेदार", "landlord", "मकान मालिक",
        "eviction", "बेदखल", "बेदखली", "registry", "रजिस्ट्री", "rera", "रेरा",
        "builder", "बिल्डर", "flat", "फ्लैट", "apartment", "house", "मकान",
        "boundary dispute", "सीमा विवाद", "encroachment", "अतिक्रमण", "lease",
        "पट्टा", "illegal possession", "अवैध कब्जा", "sale deed", "बैनामा",
        "mutation", "दाखिल खारिज", "khata", "khasra", "खसरा", "खतौनी",
        "ancestral property", "पैतृक संपत्ति", "partition", "बंटवारा",
    ]),
    ("labour", [
        "salary", "वेतन", "तनख्वाह", "wages", "मजदूरी", "employment", "job",
        "naukri", "नौकरी", "fired", "terminate", "termination", "निकाला",
        "labour", "श्रम", "pf", "epf", "provident fund", "भविष्य निधि",
        "esi", "esic", "workplace", "harassment at work", "maternity", "gratuity",
        "ग्रेच्युटी", "unpaid salary", "pending salary", "बकाया वेतन", "overtime",
        "relieving letter", "experience letter", "notice period", "contractor",
        "ठेकेदार", "employer", "नियोक्ता", "कर्मचारी", "श्रमिक", "बोनस", "bonus",
        "layoff", "retrenchment", "छंटनी",
    ]),
    ("family", [
        "divorce", "तलाक", "maintenance", "गुजारा भत्ता", "custody", "बच्चा",
        "alimony", "dowry", "दहेज", "inheritance", "विरासत", "adoption",
        "गोद लेना", "marriage", "शादी", "विवाह", "matrimonial", "separation",
        "पति", "पत्नी", "husband", "wife", "spouse", "child custody",
        "बच्चों की कस्टडी", "in-laws", "ससुराल", "succession", "उत्तराधिकार",
        "will", "वसीयत", "पारिवारिक विवाद",
    ]),
    ("criminal", [
        "fir", "police", "पुलिस", "thana", "थाना", "chowki", "चौकी",
        "arrest", "गिरफ्तार", "गिरफ्तारी", "bail", "जमानत", "theft", "चोरी",
        "fraud", "धोखा", "धोखाधड़ी", "cheating", "assault", "मारपीट",
        "complaint", "criminal", "आपराधिक", "murder", "हत्या", "cybercrime",
        "साइबर अपराध", "harassment", "उत्पीड़न", "blackmail", "ब्लैकमेल",
        "extortion", "रंगदारी", "threat", "धमकी", "upi fraud", "ऑनलाइन ठगी",
        "cyber fraud", "scam", "घोटाला", "hit and run", "accident", "हादसा",
        "police refusal", "zero fir",
    ]),
]


def keyword_classify(text: str) -> str:
    """
    Classify issue text using keyword matching with safe boundary checks.
    Uses regex word boundaries for ASCII terms to prevent substring false-positives
    (e.g., 'helpful' matching 'pf' or 'parents' matching 'rent').
    Returns a category slug. Falls back to 'other' if nothing matches.
    """
    lower = text.lower()
    for slug, keywords in _KEYWORD_MAP:
        for kw in keywords:
            if kw.isascii():
                # Word/phrase boundary matching for ASCII terms
                if re.search(r"\b" + re.escape(kw) + r"\b", lower):
                    return slug
            else:
                # Substring matching for Devanagari / Hindi characters
                if kw in lower:
                    return slug
    return "other"


# ─────────────────────────────────────────────────────────────────────────────
# Main classification function
# ─────────────────────────────────────────────────────────────────────────────

def classify_issue(issue_text: str) -> dict:
    """
    Classify a user's legal issue into a category slug.

    Tries Gemini API first. Falls back to keyword matching if:
      - GEMINI_API_KEY is not set
      - Network error or API quota exceeded
      - Gemini returns an unexpected response

    Parameters
    ----------
    issue_text : str
        The raw issue description typed by the user. NOT persisted.

    Returns
    -------
    dict with keys: slug (str), method (str), error (str)
    """
    if not issue_text or not issue_text.strip():
        return {"slug": "other", "method": "fallback", "error": "Empty input"}

    # Truncate to 800 chars to avoid excessive token usage
    safe_text = issue_text.strip()[:800]

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    # ── Try Gemini ──────────────────────────────────────────────────────────
    if api_key and api_key != "your-gemini-api-key-here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                model_name="gemini-flash-latest",
                generation_config={
                    "temperature": 0.0,        # deterministic classification
                    "max_output_tokens": 300,  # slug with thinking token headroom
                    "top_p": 1,
                },
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ],
            )

            prompt = _CLASSIFICATION_PROMPT.format(issue_text=safe_text)
            response = model.generate_content(prompt)
            raw = response.text.strip().lower()

            # Clean Markdown code fences or JSON formatting if present
            cleaned_raw = re.sub(r"```[a-zA-Z]*", "", raw).replace("```", "").strip()

            # Extract any valid slug token (handles prefixes like 'Category: consumer')
            tokens = re.findall(r"[a-z_]+", cleaned_raw)
            valid_tokens = [t for t in tokens if t in VALID_SLUGS]

            if valid_tokens:
                # If specific category slugs are present, prefer them over 'other'
                specific_tokens = [t for t in valid_tokens if t != "other"]
                slug = specific_tokens[0] if specific_tokens else valid_tokens[0]
                return {"slug": slug, "method": "gemini", "error": ""}
            else:
                # Gemini gave an unexpected response — use keyword fallback
                logger.warning("Gemini returned unexpected slug %r; using keyword fallback", raw)
                fallback_slug = keyword_classify(issue_text)
                return {"slug": fallback_slug, "method": "keyword", "error": ""}

        except Exception as exc:
            logger.error("Gemini API error: %s", exc)
            fallback_slug = keyword_classify(issue_text)
            return {
                "slug": fallback_slug,
                "method": "keyword",
                "error": f"Gemini unavailable: {type(exc).__name__}",
            }

    # ── No API key — use keyword fallback ───────────────────────────────────
    slug = keyword_classify(issue_text)
    return {
        "slug": slug,
        "method": "keyword",
        "error": "GEMINI_API_KEY not configured — using keyword classification",
    }
