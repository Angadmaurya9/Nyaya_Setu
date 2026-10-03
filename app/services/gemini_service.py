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
        "घरेलू उत्पीड़न",
    ]),
    ("consumer", [
        "consumer", "उपभोक्ता", "defective", "खराब", "refund", "वापसी",
        "product", "service", "e-commerce", "amazon", "flipkart", "online shopping",
        "cheating by company", "bill", "overcharge", "insurance claim",
    ]),
    ("property", [
        "property", "संपत्ति", "land", "जमीन", "plot", "rent", "किराया",
        "tenant", "किरायेदार", "eviction", "बेदखल", "registry", "rera",
        "boundary dispute", "encroachment", "अतिक्रमण", "lease",
    ]),
    ("family", [
        "divorce", "तलाक", "maintenance", "गुजारा भत्ता", "custody", "बच्चा",
        "alimony", "dowry", "दहेज", "inheritance", "विरासत", "adoption",
        "marriage", "शादी", "matrimonial", "separation", "husband", "wife",
    ]),
    ("labour", [
        "salary", "वेतन", "wages", "employment", "job", "naukri", "नौकरी",
        "fired", "terminate", "labour", "श्रम", "pf", "provident fund",
        "esi", "workplace", "harassment at work", "maternity", "gratuity",
    ]),
    ("rti", [
        "rti", "right to information", "सूचना का अधिकार", "information",
        "government document", "सरकारी दस्तावेज", "application rejected",
        "pio", "public information", "transparency",
    ]),
    ("criminal", [
        "fir", "police", "पुलिस", "arrest", "गिरफ्तार", "bail", "जमानत",
        "theft", "चोरी", "fraud", "धोखा", "cheating", "assault", "complaint",
        "criminal", "आपराधिक", "murder", "cybercrime", "harassment",
    ]),
]


def keyword_classify(text: str) -> str:
    """
    Classify issue text using simple keyword matching.
    Returns a category slug. Falls back to 'other' if nothing matches.
    """
    lower = text.lower()
    for slug, keywords in _KEYWORD_MAP:
        for kw in keywords:
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
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 0.0,        # deterministic classification
                    "max_output_tokens": 20,   # slug only — very short
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

            # Extract the slug (ignore any accidental extra words)
            slug = re.sub(r"[^a-z_]", "", raw.split()[0]) if raw.split() else ""

            if slug in VALID_SLUGS:
                return {"slug": slug, "method": "gemini", "error": ""}
            else:
                # Gemini gave an unexpected response — use keyword fallback
                logger.warning("Gemini returned unexpected slug %r; using keyword fallback", slug)
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
