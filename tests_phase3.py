"""
NyayaSetu — Phase 3 Test Suite: RTI Application Generator & Full Regression
===========================================================================
Tests:
  1. RTI Generator Form Access & Multilingual Rendering
  2. Form Validation & Error Handling
  3. Statutory Draft Construction (Section 6(1) compliance, fee clauses, urgency)
  4. Editable Preview Rendering & Action Controls (Print, Copy, PDF)
  5. ReportLab PDF Export (Valid binary PDF generation and download headers)
  6. Phase 1 & Phase 2 Full Regression Verification
"""

import unittest
import io
from app import create_app, db
from app.models import LegalCategory, Helpline, UserQuery
from config import TestingConfig


class Phase3RtiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_01_rti_form_renders(self):
        """Verify RTI generator form renders with all required fields in EN and HI."""
        # English
        resp_en = self.client.get("/rti/?lang=en")
        self.assertEqual(resp_en.status_code, 200)
        html_en = resp_en.data.decode("utf-8")
        self.assertIn("RTI Application Generator", html_en)
        self.assertIn("applicant_name", html_en)
        self.assertIn("public_authority", html_en)
        self.assertIn("info_requested", html_en)
        self.assertIn("fee_mode", html_en)

        # Hindi
        resp_hi = self.client.get("/rti/?lang=hi")
        self.assertEqual(resp_hi.status_code, 200)
        html_hi = resp_hi.data.decode("utf-8")
        self.assertIn("RTI आवेदन जनरेटर", html_hi)

    def test_02_rti_form_validation(self):
        """Verify missing mandatory fields trigger validation errors."""
        # Missing all required fields
        resp = self.client.post("/rti/generate", data={
            "applicant_name": "",
            "applicant_address": "",
            "public_authority": "",
            "subject": "",
            "info_requested": ""
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")
        self.assertIn("Applicant name is required", html)
        self.assertIn("Public authority", html)

    def test_03_statutory_draft_generation(self):
        """Verify complete statutory draft is created with all legal requirements."""
        data = {
            "applicant_name": "Ramesh Kumar Sharma",
            "applicant_address": "House No 42, Civil Lines, Jaipur, Rajasthan - 302006",
            "phone": "9876543210",
            "email": "ramesh@example.com",
            "public_authority": "Jaipur Development Authority (JDA)",
            "pio_designation": "The Public Information Officer (PIO)",
            "department_address": "Ram Kishore Vyas Bhavan, Indira Circle, Jawahar Lal Nehru Marg, Jaipur",
            "subject": "Sanctioned road tender and expenditure records of Ward 12",
            "info_requested": "1. Provide certified copy of the road construction tender.\n2. Provide material quality test reports.\n3. Provide copy of work completion certificate.",
            "life_liberty": "no",
            "fee_mode": "ipo",
            "fee_details": "54F 987654",
            "delivery_mode": "Speed Post",
            "date": "04/10/2026",
            "place": "Jaipur"
        }

        resp = self.client.post("/rti/generate", data=data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")

        # Must be on preview page
        self.assertIn("RTI Application Draft Preview", html)
        self.assertIn("draft-textarea", html)
        self.assertIn("Ramesh Kumar Sharma", html)
        self.assertIn("Jaipur Development Authority", html)
        self.assertIn("SECTION 6(1)", html)
        self.assertIn("Indian Postal Order (IPO)", html)
        self.assertIn("54F 987654", html)
        self.assertIn("Download as PDF", html)
        self.assertIn("window.print()", html)

    def test_04_bpl_fee_exemption_clause(self):
        """Verify BPL fee exemption clause under Section 7(5) is correctly generated."""
        data = {
            "applicant_name": "Sunita Devi",
            "applicant_address": "Village Rampur, District Varanasi, UP",
            "public_authority": "Block Development Office",
            "subject": "Panchayat development records",
            "info_requested": "Certified copy of MNREGA muster rolls.",
            "fee_mode": "bpl",
            "bpl_card_no": "BPL-UP-2024-8899",
            "date": "04/10/2026",
            "place": "Varanasi"
        }

        resp = self.client.post("/rti/generate", data=data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")
        self.assertIn("Section 7(5)", html)
        self.assertIn("Below Poverty Line (BPL)", html)
        self.assertIn("BPL-UP-2024-8899", html)

    def test_05_urgency_clause_life_or_liberty(self):
        """Verify 48-hour urgency clause under Section 7(1) is included when checked."""
        data = {
            "applicant_name": "Anita Verma",
            "applicant_address": "Delhi",
            "public_authority": "District Magistrate Office",
            "subject": "Custodial detention record",
            "info_requested": "Grounds of detention and medical report.",
            "life_liberty": "yes",
            "fee_mode": "court_fee",
            "date": "04/10/2026",
            "place": "Delhi"
        }

        resp = self.client.post("/rti/generate", data=data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")
        self.assertIn("48 hours", html)
        self.assertIn("Section 7(1)", html)

    def test_06_reportlab_pdf_export(self):
        """Verify ReportLab produces valid binary PDF with appropriate headers."""
        sample_draft = (
            "APPLICATION UNDER SECTION 6(1) OF THE RTI ACT 2005\n\n"
            "To The Public Information Officer,\n"
            "Public Works Department\n\n"
            "1. Applicant Name: Test Applicant\n"
            "2. Address: Test City\n"
            "3. Particulars of Information: Sample RTI Queries\n"
            "4. Fee Details: ₹10 IPO enclosed.\n\n"
            "Date: 04/10/2026"
        )

        resp = self.client.post("/rti/export-pdf", data={
            "draft_text": sample_draft,
            "applicant_name": "Test_Applicant"
        })

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type"), "application/pdf")
        self.assertIn("attachment; filename=RTI_Application_Test_Applicant.pdf", resp.headers.get("Content-Disposition", ""))

        # Verify binary PDF signature (%PDF-)
        pdf_bytes = resp.data
        self.assertTrue(pdf_bytes.startswith(b"%PDF-"), "Exported file is not a valid PDF")
        self.assertGreater(len(pdf_bytes), 500, "Exported PDF is suspiciously small")

    def test_07_regression_phase1_and_phase2(self):
        """Comprehensive regression test ensuring Phase 1 and Phase 2 features still function."""
        # 1. Homepage loads
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("NyayaSetu", resp.data.decode("utf-8"))

        # 2. Problem-to-Action issue form loads and accepts submission
        post_resp = self.client.post("/issue", data={
            "issue_text": "I ordered an electronic device online which stopped working and seller refuses warranty"
        }, follow_redirects=False)
        self.assertEqual(post_resp.status_code, 302)
        self.assertIn("/guidance/consumer", post_resp.headers["Location"])

        # 3. Guidance dashboard loads with action steps & RTI cross-link
        rti_guide_resp = self.client.get("/guidance/rti")
        self.assertEqual(rti_guide_resp.status_code, 200)
        html_rti = rti_guide_resp.data.decode("utf-8")
        self.assertIn("RTI", html_rti)
        self.assertIn("/rti/", html_rti)  # Link to new RTI Generator

        # 4. Standard informational pages
        for path in ["/about", "/resources", "/contact", "/legal/disclaimer", "/legal/privacy", "/legal/terms"]:
            r = self.client.get(path)
            self.assertEqual(r.status_code, 200, f"Path {path} returned {r.status_code}")


if __name__ == "__main__":
    unittest.main()
