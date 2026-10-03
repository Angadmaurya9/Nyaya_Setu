"""
NyayaSetu — Database Models (Phase 2)
======================================
Phase 2 adds three new models to the existing SiteVisit foundation:

  LegalCategory  — Taxonomy of legal issue types (property, family, etc.)
  LegalGuidance  — Verified guidance records linked to a category.
                   Each record has an official source citation and URL.
  Helpline       — Verified helpline numbers with scope descriptions.

PRIVACY NOTES:
  - UserQuery stores ONLY the identified category slug (e.g. "consumer"),
    NOT the original issue text typed by the user.
  - No personal identifying information is stored.
"""

from datetime import datetime, timezone
from app import db


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1 model (unchanged)
# ─────────────────────────────────────────────────────────────────────────────

class SiteVisit(db.Model):
    """Anonymous, aggregate visit record — no PII stored."""
    __tablename__ = "site_visits"

    id = db.Column(db.Integer, primary_key=True)
    page_path = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(10), nullable=False, default="en")
    visited_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<SiteVisit path={self.page_path!r}>"


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2 models
# ─────────────────────────────────────────────────────────────────────────────

class LegalCategory(db.Model):
    """
    A category of legal issue (e.g. 'consumer', 'property').

    slug         — machine-readable identifier used by Gemini and fallback logic
    name_en      — English display name
    name_hi      — Hindi display name
    description_en / description_hi — brief explanation shown to users
    icon         — emoji icon for UI display
    """
    __tablename__ = "legal_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_hi = db.Column(db.String(100), nullable=False)
    description_en = db.Column(db.Text, nullable=False, default="")
    description_hi = db.Column(db.Text, nullable=False, default="")
    icon = db.Column(db.String(10), nullable=False, default="⚖️")

    # Relationship: one category → many guidance records
    guidance_items = db.relationship(
        "LegalGuidance", back_populates="category", lazy="dynamic"
    )

    def __repr__(self):
        return f"<LegalCategory slug={self.slug!r}>"

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name_en": self.name_en,
            "name_hi": self.name_hi,
            "icon": self.icon,
        }


class LegalGuidance(db.Model):
    """
    A single verified guidance record for a legal category.

    Fields:
      category_id    — FK to LegalCategory
      title_en/hi    — Heading for this piece of guidance
      body_en/hi     — Plain-language explanation (≤ 300 words)
      action_steps_en/hi — Numbered action steps the user can take
      source_name    — Name of the official source (e.g. "Consumer Protection Act 2019")
      source_url     — URL to the official government resource
      verified       — Whether the record has been manually fact-checked
      order_index    — Display order within its category (lower = shown first)
    """
    __tablename__ = "legal_guidance"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("legal_categories.id"), nullable=False, index=True
    )
    title_en = db.Column(db.String(200), nullable=False)
    title_hi = db.Column(db.String(200), nullable=False)
    body_en = db.Column(db.Text, nullable=False)
    body_hi = db.Column(db.Text, nullable=False)
    action_steps_en = db.Column(db.Text, nullable=False, default="")  # JSON list stored as text
    action_steps_hi = db.Column(db.Text, nullable=False, default="")  # JSON list stored as text
    source_name = db.Column(db.String(300), nullable=False)
    source_url = db.Column(db.String(500), nullable=False, default="")
    verified = db.Column(db.Boolean, nullable=False, default=True)
    order_index = db.Column(db.Integer, nullable=False, default=0)

    category = db.relationship("LegalCategory", back_populates="guidance_items")

    def __repr__(self):
        return f"<LegalGuidance id={self.id} category_id={self.category_id}>"

    def get_action_steps(self, lang="en"):
        """Parse the JSON-encoded action steps and return a Python list."""
        import json
        raw = self.action_steps_en if lang == "en" else self.action_steps_hi
        try:
            steps = json.loads(raw)
            return steps if isinstance(steps, list) else []
        except (json.JSONDecodeError, TypeError):
            return []


class Helpline(db.Model):
    """
    A verified helpline number with scope and language info.
    """
    __tablename__ = "helplines"

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(200), nullable=False)
    name_hi = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(30), nullable=False)
    scope_en = db.Column(db.String(300), nullable=False, default="")
    scope_hi = db.Column(db.String(300), nullable=False, default="")
    # Comma-separated category slugs this helpline is relevant to (empty = all)
    relevant_categories = db.Column(db.String(500), nullable=False, default="")
    source_url = db.Column(db.String(500), nullable=False, default="")

    def __repr__(self):
        return f"<Helpline {self.number} name={self.name_en!r}>"

    def is_relevant_to(self, slug: str) -> bool:
        """Return True if this helpline applies to the given category slug."""
        cats = [c.strip() for c in self.relevant_categories.split(",") if c.strip()]
        return not cats or slug in cats


class UserQuery(db.Model):
    """
    An anonymised record of a guidance request.

    PRIVACY: Only the category slug (e.g. "consumer") is stored.
    The original issue text is NEVER persisted.
    """
    __tablename__ = "user_queries"

    id = db.Column(db.Integer, primary_key=True)
    category_slug = db.Column(db.String(50), nullable=False, index=True)
    # 'gemini' if AI classified, 'keyword' if fallback was used
    classification_method = db.Column(db.String(20), nullable=False, default="keyword")
    language = db.Column(db.String(10), nullable=False, default="en")
    queried_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<UserQuery slug={self.category_slug!r} method={self.classification_method!r}>"
