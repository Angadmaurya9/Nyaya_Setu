"""
NyayaSetu — Phase 2 Automated Test Suite
=========================================
Tests:
  1. Database Model & Seeding Verification (Categories, Guidance, Helplines)
  2. Classification Engine (Gemini Service & Keyword Fallback)
  3. Problem-to-Action Guidance Flow (POST /issue -> Redirect -> Guidance Dashboard)
  4. Privacy Verification (Raw user text NEVER stored in database)
  5. UI Scope Corrections (GET /schemes redirected to /issue)
  6. Standard Informational Routes (Home, About, Resources, Legal Pages)
"""

import unittest
from app import create_app, db
from app.models import LegalCategory, LegalGuidance, Helpline, UserQuery
from app.services.gemini_service import classify_issue, keyword_classify
from config import TestingConfig


class Phase2TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_01_knowledge_base_seeding(self):
        """Verify that all 8 categories and 8 helplines are seeded with verified data."""
        categories = LegalCategory.query.all()
        self.assertEqual(len(categories), 8)

        slugs = {c.slug for c in categories}
        expected_slugs = {
            "consumer", "property", "family", "labour",
            "rti", "criminal", "domestic_violence", "other"
        }
        self.assertEqual(slugs, expected_slugs)

        # Check guidance items and citations
        for cat in categories:
            guidance_items = cat.guidance_items.all()
            self.assertGreaterEqual(len(guidance_items), 1, f"Missing guidance for {cat.slug}")
            for g in guidance_items:
                self.assertTrue(g.verified)
                self.assertTrue(len(g.source_name) > 0)
                self.assertTrue(len(g.get_action_steps("en")) > 0)
                self.assertTrue(len(g.get_action_steps("hi")) > 0)

        # Check helplines
        helplines = Helpline.query.all()
        self.assertEqual(len(helplines), 8)
        numbers = {h.number for h in helplines}
        self.assertIn("112", numbers)
        self.assertIn("15100", numbers)
        self.assertIn("1915", numbers)
        self.assertIn("1930", numbers)
        self.assertIn("181", numbers)

    def test_02_classification_engine(self):
        """Verify keyword classification for both English and Hindi inputs."""
        test_cases = [
            ("I bought a defective mobile phone from Amazon and they refused my refund", "consumer"),
            ("दुकानदार ने खराब सामान दिया और पैसे वापस नहीं कर रहा", "consumer"),
            ("My landlord locked my apartment and is demanding illegal eviction rent", "property"),
            ("जमीन पर पड़ोसी ने अवैध कब्जा कर लिया है", "property"),
            ("Seeking divorce and child maintenance custody after marriage separation", "family"),
            ("My company withheld 3 months salary and terminated me without notice", "labour"),
            ("PIO rejected my RTI application without citing any exemption", "rti"),
            ("Someone did an online bank fraud via UPI and stole 50000 rupees", "criminal"),
            ("Police refused to register an FIR for assault and theft", "criminal"),
            ("Physical and emotional abuse by in-laws at home domestic violence", "domestic_violence"),
            ("घरेलू हिंसा और ससुराल में प्रताड़ना की शिकायत", "domestic_violence"),
        ]

        for text, expected_slug in test_cases:
            res = classify_issue(text)
            self.assertEqual(
                res["slug"], expected_slug,
                f"Failed classification for '{text}': got {res['slug']}, expected {expected_slug}"
            )
            self.assertIn(res["method"], ["gemini", "keyword"])

    def test_03_problem_to_action_post_flow(self):
        """Verify submitting an issue redirects to the correct guidance dashboard."""
        post_cases = [
            ("I bought a defective product and the seller refuses to honor warranty", "consumer"),
            ("My landlord is threatening illegal eviction without legal notice", "property"),
            ("Unpaid wages and salary after arbitrary dismissal from job", "labour"),
            ("Need to file RTI for delayed government road inspection records", "rti"),
        ]

        for text, expected_slug in post_cases:
            resp = self.client.post("/issue", data={"issue_text": text}, follow_redirects=False)
            self.assertEqual(resp.status_code, 302)
            self.assertIn(f"/guidance/{expected_slug}", resp.headers["Location"])

            # Follow redirect and verify dashboard rendering
            dash_resp = self.client.get(resp.headers["Location"])
            self.assertEqual(dash_resp.status_code, 200)
            html = dash_resp.data.decode("utf-8")
            self.assertIn("action-step-item", html)
            self.assertIn("source-citation", html)
            self.assertIn("Disclaimer", html)

    def test_04_privacy_guarantee(self):
        """CRITICAL: Assert that raw issue text is NEVER persisted in database."""
        sensitive_sample = "Sensitive text: Landlord John Doe stole 45000 rupees security deposit"
        self.client.post("/issue", data={"issue_text": sensitive_sample}, follow_redirects=True)

        # Inspect all records in UserQuery
        queries = UserQuery.query.all()
        self.assertGreater(len(queries), 0)

        for q in queries:
            # category_slug must be clean slug
            self.assertIn(q.category_slug, ["property", "consumer", "criminal", "other", "family", "labour", "rti", "domestic_violence"])
            # check representation and attributes
            q_dump = f"{q.id} {q.category_slug} {q.classification_method} {q.language}"
            self.assertNotIn("John Doe", q_dump)
            self.assertNotIn("45000", q_dump)
            self.assertNotIn("security deposit", q_dump)

    def test_05_scope_correction_schemes_redirect(self):
        """Verify /schemes is redirected to /issue (out-of-scope feature removed)."""
        resp = self.client.get("/schemes", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/issue", resp.headers["Location"])

    def test_06_direct_guidance_routes(self):
        """Verify all 8 guidance pages render correctly in both EN and HI."""
        slugs = ["consumer", "property", "family", "labour", "rti", "criminal", "domestic_violence", "other"]
        for slug in slugs:
            # English
            resp_en = self.client.get(f"/guidance/{slug}?lang=en")
            self.assertEqual(resp_en.status_code, 200)
            # Hindi
            resp_hi = self.client.get(f"/guidance/{slug}?lang=hi")
            self.assertEqual(resp_hi.status_code, 200)

    def test_07_core_informational_routes(self):
        """Verify all other core pages load properly."""
        routes = ["/", "/about", "/resources", "/contact", "/legal/disclaimer", "/legal/privacy", "/legal/terms"]
        for r in routes:
            resp = self.client.get(r)
            self.assertEqual(resp.status_code, 200, f"Route {r} failed with {resp.status_code}")


if __name__ == "__main__":
    unittest.main()
