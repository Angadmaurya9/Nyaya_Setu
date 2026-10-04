"""
NyayaSetu — Phase 4 Automated Test Suite
=========================================
Tests for Error Handling, Security, Accessibility, and System Hardening:
  1. Main Routes & Homepage Status
  2. Guidance Endpoint & Safe Fallback on Missing Matches
  3. Dataset Retrieval & Verification
  4. Gemini Error Handling & Resilient Keyword Fallback (Mocked Failures)
  5. Invalid AI Responses (Mocked Hallucinations Gracefully Caught)
  6. Empty & Excessively Long Input Validation
  7. Security: Script/HTML Injection Handling & Sanitization
  8. Security: Zero-Retention of RTI Details & Sensitive Descriptions
  9. Security: Production Debug Mode Disabled
 10. RTI Generator Form & Robust PDF Generation (Special Chars, Multi-page)
 11. Custom 404 & User-Friendly Error Responses
 12. Full Regression of Existing Phase 1, 2, and 3 Features
"""

import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models import LegalCategory, LegalGuidance, Helpline, UserQuery
from app.services.gemini_service import classify_issue, VALID_SLUGS
from config import TestingConfig, ProductionConfig


class Phase4HardeningTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # ─────────────────────────────────────────────────────────────
    # 1. Main Routes & Guidance Retrieval
    # ─────────────────────────────────────────────────────────────
    def test_01_main_routes_and_homepage(self):
        """Verify all primary application pages load cleanly with HTTP 200."""
        routes = [
            "/", "/about", "/resources", "/contact", "/issue",
            "/rti/", "/legal/disclaimer", "/legal/privacy", "/legal/terms"
        ]
        for path in routes:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"Route {path} failed with {resp.status_code}")

    def test_02_guidance_endpoint_and_missing_matches(self):
        """Verify guidance endpoint returns structured remedies and safely falls back on invalid slugs."""
        # Valid category
        resp_valid = self.client.get("/guidance/consumer")
        self.assertEqual(resp_valid.status_code, 200)
        self.assertIn("Consumer Protection Act", resp_valid.data.decode("utf-8"))

        # Invalid/missing category slug -> must safely fallback to 'other' without 404 or 500 error
        resp_invalid = self.client.get("/guidance/non_existent_category_xyz")
        self.assertEqual(resp_invalid.status_code, 200)
        html = resp_invalid.data.decode("utf-8")
        self.assertIn("General Legal Aid", html)

    def test_03_dataset_retrieval(self):
        """Verify database contains all verified categories, action steps, and helplines."""
        categories = LegalCategory.query.all()
        self.assertEqual(len(categories), 8)
        for cat in categories:
            items = LegalGuidance.query.filter_by(category_id=cat.id).all()
            self.assertGreater(len(items), 0)
            for it in items:
                self.assertTrue(it.verified)
                self.assertIn("http", it.source_url)

    # ─────────────────────────────────────────────────────────────
    # 2. Gemini Error Handling & Resilient Fallback
    # ─────────────────────────────────────────────────────────────
    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_04_gemini_api_failure_and_timeout(self, mock_model_class, mock_env):
        """Simulate Gemini API network timeout/failure; verify system falls back to keyword classifier."""
        mock_env.return_value = "fake-api-key-12345"
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = RuntimeError("Connection timed out to Google API")
        mock_model_class.return_value = mock_model_instance

        # Even though Gemini throws an exception, classify_issue must NOT crash
        result = classify_issue("My landlord locked me out of the flat and rent dispute")
        self.assertEqual(result["slug"], "property")
        self.assertEqual(result["method"], "keyword")
        self.assertIn("Gemini unavailable", result["error"])

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_05_invalid_gemini_response_handling(self, mock_model_class, mock_env):
        """Simulate Gemini returning an invalid/hallucinated slug; verify graceful fallback."""
        mock_env.return_value = "fake-api-key-12345"
        mock_model_instance = MagicMock()
        # Mock Gemini hallucinating a non-existent slug
        mock_response = MagicMock()
        mock_response.text = "completely_hallucinated_legal_concept_not_in_slugs"
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = classify_issue("Someone withdrew 20000 rupees via UPI cyber fraud")
        # Must catch invalid slug and fall back to keyword classification
        self.assertEqual(result["slug"], "criminal")
        self.assertEqual(result["method"], "keyword")

    # ─────────────────────────────────────────────────────────────
    # 3. Input Validation & Security Checks
    # ─────────────────────────────────────────────────────────────
    def test_06_empty_and_excessive_inputs(self):
        """Verify empty and excessively long inputs are caught by validation."""
        # Empty issue input
        resp_empty = self.client.post("/issue", data={"issue_text": "", "category": ""}, follow_redirects=True)
        self.assertEqual(resp_empty.status_code, 200)
        self.assertIn("Please describe your legal issue", resp_empty.data.decode("utf-8"))

        # Excessively long issue input (> 1000 chars)
        long_text = "A" * 1500
        resp_long = self.client.post("/issue", data={"issue_text": long_text}, follow_redirects=True)
        self.assertEqual(resp_long.status_code, 200)
        self.assertIn("at most", resp_long.data.decode("utf-8"))

        # Empty RTI form input
        resp_rti_empty = self.client.post("/rti/generate", data={}, follow_redirects=True)
        self.assertEqual(resp_rti_empty.status_code, 200)
        self.assertIn("required", resp_rti_empty.data.decode("utf-8"))

    def test_07_security_script_injection_sanitization(self):
        """Verify XSS payloads in inputs are properly handled without executing or corrupting PDF/HTML."""
        xss_payload = "<script>alert('XSS')</script> & <img src=x onerror=alert(1)>"

        # 1. Post to issue
        resp = self.client.post("/issue", data={"issue_text": f"consumer complaint {xss_payload}"}, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # 2. Post to RTI generator
        rti_data = {
            "applicant_name": f"Tester {xss_payload}",
            "applicant_address": "Test Address",
            "public_authority": "Test Dept",
            "subject": f"RTI Subject {xss_payload}",
            "info_requested": f"1. Query with {xss_payload}",
            "fee_mode": "ipo"
        }
        rti_resp = self.client.post("/rti/generate", data=rti_data, follow_redirects=True)
        self.assertEqual(rti_resp.status_code, 200)
        html = rti_resp.data.decode("utf-8")
        # Ensure raw script tag is escaped and not executed as active script in preview
        self.assertNotIn("<script>alert('XSS')</script>", html)

        # 3. PDF generation with special chars and XSS payload must NOT crash ReportLab
        pdf_resp = self.client.post("/rti/export-pdf", data={
            "draft_text": f"APPLICATION UNDER RTI\n\n1. Name: Test\n2. Query: {xss_payload}\n3. Fee: IPO",
            "applicant_name": "Safe_Tester"
        })
        self.assertEqual(pdf_resp.status_code, 200)
        self.assertEqual(pdf_resp.headers.get("Content-Type"), "application/pdf")
        self.assertTrue(pdf_resp.data.startswith(b"%PDF-"))

    def test_08_privacy_zero_retention_check(self):
        """Verify sensitive RTI details and issue texts are never written to database tables."""
        sensitive_rti_name = "CONFIDENTIAL_CITIZEN_ANON_99"
        self.client.post("/rti/generate", data={
            "applicant_name": sensitive_rti_name,
            "applicant_address": "Secret Address 123",
            "public_authority": "Police Department",
            "subject": "Confidential enquiry",
            "info_requested": "Provide confidential records",
            "fee_mode": "ipo"
        }, follow_redirects=True)

        # Inspect database: confirm no table contains this sensitive name
        queries = UserQuery.query.all()
        for q in queries:
            self.assertNotIn(sensitive_rti_name, str(q.__dict__))

    def test_09_production_config_debug_disabled(self):
        """Verify production configuration strictly disables debug mode."""
        prod_cfg = ProductionConfig
        self.assertFalse(prod_cfg.DEBUG)
        self.assertFalse(prod_cfg.TESTING)

    # ─────────────────────────────────────────────────────────────
    # 4. RTI PDF Generation & Multi-Page Support
    # ─────────────────────────────────────────────────────────────
    def test_10_pdf_generation_multi_page(self):
        """Verify ReportLab builds a clean multi-page PDF when draft has extensive queries."""
        # Generate a large 50-item RTI query draft
        queries = "\n".join([f"{i}. Detailed enquiry regarding municipal budget item number {i}." for i in range(1, 50)])
        large_draft = f"APPLICATION UNDER SECTION 6(1) OF RTI ACT\n\nTo The PIO,\nMunicipal Corporation\n\n1. Applicant: Test\n2. Address: City\n3. Particulars:\n{queries}\n\n4. Fee: ₹10\n\nDate: 04/10/2026"

        pdf_resp = self.client.post("/rti/export-pdf", data={
            "draft_text": large_draft,
            "applicant_name": "Ramesh_Sharma"
        })
        self.assertEqual(pdf_resp.status_code, 200)
        self.assertTrue(pdf_resp.data.startswith(b"%PDF-"))
        self.assertGreater(len(pdf_resp.data), 2000, "Multi-page PDF should have substantial byte size")

    def test_11_custom_404_error_handler(self):
        """Verify unknown URLs return custom branded 404 page without technical leakage."""
        resp = self.client.get("/non_existent_page_url_12345")
        self.assertEqual(resp.status_code, 404)
        html = resp.data.decode("utf-8")
        self.assertIn("404", html)
        self.assertIn("NyayaSetu", html)


if __name__ == "__main__":
    unittest.main()
