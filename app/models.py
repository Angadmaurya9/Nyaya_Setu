"""
NyayaSetu — Database Models (Phase 1 Foundation)
=================================================
This module defines the SQLAlchemy ORM models.

Phase 1 contains only a skeleton model (SiteVisit) to prove that the
database layer initialises correctly.  Real models (UserQuery, Scheme,
Resource, etc.) will be added in Phase 2.

PRIVACY NOTE:
- Do NOT store sensitive user issue descriptions or personal identifiers.
- SiteVisit logs only aggregate-friendly, anonymous data.
"""

from datetime import datetime, timezone
from app import db  # 'db' is the SQLAlchemy instance created in app/__init__.py


class SiteVisit(db.Model):
    """
    Anonymous, aggregate visit record.

    Stores only the page path, preferred language, and timestamp.
    No IP address, cookies, or personal data are stored.
    This is used solely to understand which pages are accessed most often.
    """

    __tablename__ = "site_visits"

    id = db.Column(db.Integer, primary_key=True)
    page_path = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(10), nullable=False, default="en")
    visited_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<SiteVisit path={self.page_path!r} lang={self.language!r}>"

    def to_dict(self) -> dict:
        """Serialise to a plain dictionary (useful for JSON responses later)."""
        return {
            "id": self.id,
            "page_path": self.page_path,
            "language": self.language,
            "visited_at": self.visited_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# Phase 2 placeholders (not implemented yet — kept as comments for clarity)
# ---------------------------------------------------------------------------
# class Scheme(db.Model):
#     """Government welfare / legal-aid scheme information."""
#     ...
#
# class Resource(db.Model):
#     """Legal resource links and documents."""
#     ...
#
# class ContactMessage(db.Model):
#     """Non-sensitive contact-form submissions (no issue text stored)."""
#     ...
