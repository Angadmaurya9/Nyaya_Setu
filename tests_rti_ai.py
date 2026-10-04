"""
NyayaSetu — RTI AI Question Generator Automated Tests (tests_rti_ai.py)
========================================================================
Comprehensive automated tests for Phase 1 backend AI integration:
  1. Service unit test: English question generation (mocked Gemini)
  2. Service unit test: Hindi question generation (mocked Gemini)
  3. Service unit test: Input validation (empty, whitespace, too short, non-string)
  4. Service unit test: Missing / invalid API key handling
  5. Service unit test: Malformed JSON output from model
  6. Service unit test: Empty output from model
  7. Service unit test: API exception / timeout handling
  8. Endpoint test: POST /rti/suggest-questions with JSON payload (HTTP 200)
  9. Endpoint test: POST /rti/suggest-questions with form payload (HTTP 200)
 10. Endpoint test: Input validation - missing / empty / too short (HTTP 400)
 11. Endpoint test: Input validation - excessive length > 1000 chars (HTTP 400)
 12. Endpoint test: Error propagation when AI service fails (HTTP 503)
 13. Security & Privacy: Zero retention of descriptions in database
 14. Non-regression: classify_issue() continues working as expected
 15. Non-regression: Existing RTI generator, preview, and PDF export intact
"""

import unittest
import json
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models import UserQuery
from app.services.gemini_service import (
    generate_rti_questions, classify_issue, VALID_SLUGS
)
from config import TestingConfig


class RtiAiBackendTestCase(unittest.TestCase):

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
    # 1. Service Layer Tests (gemini_service.generate_rti_questions)
    # ─────────────────────────────────────────────────────────────

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_01_service_success_english(self, mock_model_class, mock_env):
        """Verify successful generation of RTI subject and questions in English."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "subject": "Information regarding road construction and repair on MG Road",
            "questions": [
                "1. Certified copy of the work order and contract agreement for MG Road repairs.",
                "2. Certified copy of the measurement book and completion certificate.",
                "3. Details of total expenditure incurred and names of supervising engineers."
            ]
        })
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        desc = "The road construction on MG Road started 6 months ago but was left incomplete with potholes."
        result = generate_rti_questions(desc, lang="en")

        self.assertTrue(result["success"])
        self.assertEqual(result["subject"], "Information regarding road construction and repair on MG Road")
        self.assertEqual(len(result["questions"]), 3)
        # Verify leading numbers are stripped cleanly
        self.assertTrue(result["questions"][0].startswith("Certified copy of the work order"))
        self.assertEqual(result["error"], "")

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_02_service_success_hindi(self, mock_model_class, mock_env):
        """Verify successful generation of RTI subject and questions in Hindi."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "subject": "एमजी रोड सड़क निर्माण और मरम्मत कार्य के संबंध में सूचना",
            "questions": [
                "1. एमजी रोड मरम्मत कार्य के वर्क आर्डर और अनुबंध की प्रमाणित प्रति।",
                "2. कार्य की माप पुस्तिका (Measurement Book) एवं निरीक्षण रिपोर्ट की प्रति।",
                "3. परियोजना पर हुए कुल व्यय और ठेकेदार के विवरण की प्रति।"
            ]
        })
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        desc = "हमारे गांव में एमजी रोड का निर्माण अधूरा छोड़ दिया गया है और गड्ढे हो गए हैं।"
        result = generate_rti_questions(desc, lang="hi")

        self.assertTrue(result["success"])
        self.assertIn("एमजी रोड", result["subject"])
        self.assertEqual(len(result["questions"]), 3)
        self.assertTrue(result["questions"][0].startswith("एमजी रोड मरम्मत"))
        self.assertEqual(result["error"], "")

    def test_03_service_validation_empty_and_short(self):
        """Verify service rejects empty, whitespace, and short descriptions."""
        # Empty
        res_empty = generate_rti_questions("")
        self.assertFalse(res_empty["success"])
        self.assertIn("Description is required", res_empty["error"])

        # Whitespace
        res_ws = generate_rti_questions("     ")
        self.assertFalse(res_ws["success"])
        self.assertIn("Description is required", res_ws["error"])

        # Too short (< 10 chars)
        res_short = generate_rti_questions("pothole")
        self.assertFalse(res_short["success"])
        self.assertIn("at least 10 characters", res_short["error"])

        # None / non-string
        res_none = generate_rti_questions(None)
        self.assertFalse(res_none["success"])

    @patch("os.environ.get")
    def test_04_service_missing_api_key(self, mock_env):
        """Verify service returns clear error when GEMINI_API_KEY is not configured."""
        mock_env.return_value = ""
        result = generate_rti_questions("Road construction incomplete for 6 months")
        self.assertFalse(result["success"])
        self.assertIn("API KEY IS NOT CONFIGURED", result["error"].upper())
        self.assertEqual(result["subject"], "")
        self.assertEqual(result["questions"], [])

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_05_service_malformed_json_response(self, mock_model_class, mock_env):
        """Verify service safely handles unparseable / malformed model responses."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Here are your RTI questions: 1. Ask the PIO why work stopped."
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("Road construction incomplete for 6 months")
        self.assertFalse(result["success"])
        self.assertIn("malformed", result["error"].lower())

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_06_service_empty_model_response(self, mock_model_class, mock_env):
        """Verify service safely handles empty string returned by model."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = ""
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("Road construction incomplete for 6 months")
        self.assertFalse(result["success"])
        self.assertIn("empty", result["error"].lower())

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_07_service_api_exception(self, mock_model_class, mock_env):
        """Verify service handles runtime exceptions (network timeout, rate limit) gracefully."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = RuntimeError("Quota exceeded or network timeout")
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("Road construction incomplete for 6 months")
        self.assertFalse(result["success"])
        self.assertIn("AI service unavailable", result["error"])

    # ─────────────────────────────────────────────────────────────
    # 2. Endpoint Tests (POST /rti/suggest-questions)
    # ─────────────────────────────────────────────────────────────

    @patch("app.routes.rti.generate_rti_questions")
    def test_08_endpoint_success_json(self, mock_gen):
        """Verify POST /rti/suggest-questions returns 200 with JSON payload."""
        mock_gen.return_value = {
            "success": True,
            "subject": "Information regarding streetlight maintenance in Ward 12",
            "questions": [
                "Certified copy of work order for streetlight installation.",
                "Inspection reports of non-functional streetlights."
            ],
            "error": ""
        }

        resp = self.client.post(
            "/rti/suggest-questions",
            json={
                "description": "Streetlights in Ward 12 have not been working for two months despite complaints.",
                "lang": "en"
            }
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["subject"], "Information regarding streetlight maintenance in Ward 12")
        self.assertEqual(len(data["data"]["questions"]), 2)

    @patch("app.routes.rti.generate_rti_questions")
    def test_09_endpoint_success_form(self, mock_gen):
        """Verify POST /rti/suggest-questions handles standard form-encoded requests."""
        mock_gen.return_value = {
            "success": True,
            "subject": "सड़क निर्माण के संबंध में सूचना",
            "questions": ["कार्य आदेश की प्रति।"],
            "error": ""
        }

        resp = self.client.post(
            "/rti/suggest-questions",
            data={
                "description": "हमारे क्षेत्र में सड़क निर्माण 6 माह से बंद है।",
                "lang": "hi"
            }
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["subject"], "सड़क निर्माण के संबंध में सूचना")

    def test_10_endpoint_validation_empty_and_short(self):
        """Verify endpoint returns 400 when description is missing, empty, or <10 chars."""
        # Missing description
        r1 = self.client.post("/rti/suggest-questions", json={})
        self.assertEqual(r1.status_code, 400)
        self.assertFalse(r1.get_json()["success"])

        # Empty description
        r2 = self.client.post("/rti/suggest-questions", json={"description": ""})
        self.assertEqual(r2.status_code, 400)
        self.assertFalse(r2.get_json()["success"])

        # Short description (< 10 chars)
        r3 = self.client.post("/rti/suggest-questions", json={"description": "fix road"})
        self.assertEqual(r3.status_code, 400)
        self.assertIn("at least 10 characters", r3.get_json()["error"])

    def test_11_endpoint_validation_excessive_length(self):
        """Verify endpoint returns 400 when description exceeds 1000 characters."""
        long_desc = "RTI request details " * 60  # > 1000 chars
        resp = self.client.post("/rti/suggest-questions", json={"description": long_desc})
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertFalse(data["success"])
        self.assertIn("1000 characters", data["error"])

    @patch("app.routes.rti.generate_rti_questions")
    def test_12_endpoint_service_unavailable(self, mock_gen):
        """Verify endpoint returns 503 when AI service fails."""
        mock_gen.return_value = {
            "success": False,
            "subject": "",
            "questions": [],
            "error": "AI service unavailable: Quota exceeded"
        }

        resp = self.client.post(
            "/rti/suggest-questions",
            json={"description": "Enquiry regarding water pipeline repair delay"}
        )
        self.assertEqual(resp.status_code, 503)
        data = resp.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Quota exceeded", data["error"])

    # ─────────────────────────────────────────────────────────────
    # 3. Privacy, Security & Non-Regression Tests
    # ─────────────────────────────────────────────────────────────

    @patch("app.routes.rti.generate_rti_questions")
    def test_13_privacy_zero_retention(self, mock_gen):
        """Verify sensitive descriptions sent to /suggest-questions are not persisted."""
        mock_gen.return_value = {
            "success": True,
            "subject": "Safe Subject",
            "questions": ["Safe question"],
            "error": ""
        }
        secret_token = "CONFIDENTIAL_CITIZEN_TOKEN_XYZ_98765"
        self.client.post(
            "/rti/suggest-questions",
            json={"description": f"Details about {secret_token} for municipal records"}
        )

        # Check database: confirm token does not exist anywhere in UserQuery
        for query in UserQuery.query.all():
            self.assertNotIn(secret_token, str(query.__dict__))

    @patch("os.environ.get")
    def test_14_existing_classify_issue_unaffected(self, mock_env):
        """Verify classify_issue() continues to operate with its keyword fallback and valid slugs."""
        mock_env.return_value = ""  # exercise deterministic keyword fallback
        result = classify_issue("My landlord has locked me out of the rented room")
        self.assertEqual(result["slug"], "property")
        self.assertIn(result["slug"], VALID_SLUGS)

    def test_15_existing_rti_flow_unaffected(self):
        """Verify GET /rti/, POST /rti/generate, and POST /rti/export-pdf function normally."""
        # 1. Generator page loads
        resp_gen = self.client.get("/rti/")
        self.assertEqual(resp_gen.status_code, 200)
        self.assertIn("RTI", resp_gen.data.decode("utf-8"))

        # 2. Preview generation
        form_data = {
            "applicant_name": "Test Citizen",
            "applicant_address": "Test Colony, Delhi",
            "public_authority": "Municipal Corporation of Delhi",
            "subject": "Regarding sanitation inspection records",
            "info_requested": "1. Provide certified copy of sanitation roster.",
            "fee_mode": "ipo"
        }
        resp_preview = self.client.post("/rti/generate", data=form_data)
        self.assertEqual(resp_preview.status_code, 200)
        self.assertIn("Test Citizen", resp_preview.data.decode("utf-8"))

        # 3. PDF export
        resp_pdf = self.client.post("/rti/export-pdf", data={
            "draft_text": "APPLICATION UNDER RTI ACT 2005\n\n1. Name: Test Citizen\n2. Subject: Sanitation\n3. Points:\n1. Roster copy",
            "applicant_name": "Test_Citizen"
        })
        self.assertEqual(resp_pdf.status_code, 200)
        self.assertEqual(resp_pdf.headers.get("Content-Type"), "application/pdf")
        self.assertTrue(resp_pdf.data.startswith(b"%PDF-"))

    # ─────────────────────────────────────────────────────────────
    # 4. Phase 2 Frontend Integration Tests
    # ─────────────────────────────────────────────────────────────

    def test_16_frontend_elements_present_en(self):
        """Verify generator page renders AI assistant card and query controls in English."""
        resp = self.client.get("/rti/")
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")

        # Verify AI Assistant UI elements
        self.assertIn("ai-assistant-card", html)
        self.assertIn("ai_description", html)
        self.assertIn("btn-generate-questions", html)
        self.assertIn("ai-error-box", html)
        self.assertIn("ai-success-box", html)
        self.assertIn("What information do you need?", html)
        self.assertIn("Generate RTI Questions", html)

        # Verify Query Control Buttons
        self.assertIn("btn-add-query", html)
        self.assertIn("btn-remove-last-query", html)

    def test_17_frontend_elements_present_hi(self):
        """Verify generator page renders AI assistant card in Hindi when ?lang=hi."""
        resp = self.client.get("/rti/?lang=hi")
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")

        # Verify Hindi labels and helper text
        self.assertIn("आपको किस सूचना की आवश्यकता है?", html)
        self.assertIn("वैकल्पिक AI सहायक", html)
        self.assertIn("प्रश्न जोड़ें", html)
        self.assertIn("अंतिम प्रश्न हटाएं", html)

    def test_18_static_assets_contain_ai_logic(self):
        """Verify main.js and main.css contain the RTI AI frontend logic and styling."""
        with open("app/static/js/main.js", "r", encoding="utf-8") as f:
            js_code = f.read()
        self.assertIn("btn-generate-questions", js_code)
        self.assertIn("/rti/suggest-questions", js_code)
        self.assertIn("window.confirm", js_code)
        self.assertIn("btn-add-query", js_code)
        self.assertIn("btn-remove-last-query", js_code)

        with open("app/static/css/main.css", "r", encoding="utf-8") as f:
            css_code = f.read()
        self.assertIn(".ai-assistant-card", css_code)
        self.assertIn(".query-actions-btn", css_code)

    # ─────────────────────────────────────────────────────────────
    # 5. Phase 3 End-to-End Workflow & Edge Case Tests
    # ─────────────────────────────────────────────────────────────

    @patch("app.routes.rti.generate_rti_questions")
    def test_19_e2e_complete_workflow_english(self, mock_gen):
        """Complete user journey in English: generator -> AI generation -> edit -> preview -> PDF export."""
        # 1. Generator page load
        r_page = self.client.get("/rti/")
        self.assertEqual(r_page.status_code, 200)

        # 2 & 3. AI question suggestion
        mock_gen.return_value = {
            "success": True,
            "subject": "Seeking records regarding water pipeline installation in Sector 4",
            "questions": [
                "Certified copy of administrative approval and financial sanction.",
                "Inspection reports of installed pipelines and pressure tests.",
                "Details of funds disbursed to the contractor till date."
            ],
            "error": ""
        }
        r_suggest = self.client.post("/rti/suggest-questions", json={
            "description": "The water pipeline project in Sector 4 was started 8 months ago and stopped abruptly.",
            "lang": "en"
        })
        self.assertEqual(r_suggest.status_code, 200)
        sug_data = r_suggest.get_json()["data"]

        # 4 & 5. Simulate citizen editing subject and adding an additional query
        edited_subject = sug_data["subject"] + " (Revised)"
        # Format queries line by line as client JavaScript does
        queries_list = [f"{i+1}. {q}" for i, q in enumerate(sug_data["questions"])]
        # Citizen adds an additional query (using + Add Query button)
        queries_list.append("4. Daily progress diary maintained by Junior Engineer.")
        edited_queries = "\n".join(queries_list)

        # 6 & 7. Form submission -> preview generation
        form_payload = {
            "applicant_name": "Ramesh Chandra Sharma",
            "applicant_address": "Flat 302, Green Enclave, Sector 4, Noida, UP - 201301",
            "phone": "9876543210",
            "email": "ramesh.sharma@example.com",
            "public_authority": "Noida Development Authority",
            "pio_designation": "The Public Information Officer (Water Works)",
            "department_address": "Main Office, Sector 6, Noida",
            "subject": edited_subject,
            "info_requested": edited_queries,
            "fee_mode": "ipo",
            "fee_details": "45F 889900",
            "delivery_mode": "Speed Post"
        }
        r_preview = self.client.post("/rti/generate", data=form_payload)
        self.assertEqual(r_preview.status_code, 200)
        preview_html = r_preview.data.decode("utf-8")
        self.assertIn("Ramesh Chandra Sharma", preview_html)
        self.assertIn(edited_subject, preview_html)
        self.assertIn("Daily progress diary", preview_html)

        # 8. Export PDF
        # Extract draft text or submit preview draft
        from app.routes.rti import build_rti_text
        draft_text = build_rti_text(form_payload)
        r_pdf = self.client.post("/rti/export-pdf", data={
            "draft_text": draft_text,
            "applicant_name": "Ramesh_Chandra_Sharma"
        })
        self.assertEqual(r_pdf.status_code, 200)
        self.assertEqual(r_pdf.headers.get("Content-Type"), "application/pdf")
        self.assertTrue(r_pdf.data.startswith(b"%PDF-"))

    @patch("app.routes.rti.generate_rti_questions")
    def test_20_e2e_complete_workflow_hindi(self, mock_gen):
        """Complete user journey in Hindi: generator -> AI generation -> preview -> PDF export."""
        # 1. Hindi generator page load
        r_page = self.client.get("/rti/?lang=hi")
        self.assertEqual(r_page.status_code, 200)
        self.assertIn("आवेदन जनरेटर", r_page.data.decode("utf-8"))

        # 2 & 3. AI question suggestion in Hindi
        mock_gen.return_value = {
            "success": True,
            "subject": "वार्ड 15 में सीवर लाइन निर्माण कार्य के संबंध में सूचना",
            "questions": [
                "सीवर लाइन निर्माण के स्वीकृत प्रस्ताव एवं कार्य आदेश की प्रमाणित प्रति।",
                "कार्य की माप पुस्तिका एवं गुणवत्ता जांच रिपोर्ट की प्रतिलिपि।",
                "ठेकेदार को किए गए भुगतान का वाउचर-वार विवरण।"
            ],
            "error": ""
        }
        r_suggest = self.client.post("/rti/suggest-questions", json={
            "description": "हमारे वार्ड 15 में सीवर लाइन का कार्य अधूरा पड़ा है और गंदा पानी बह रहा है।",
            "lang": "hi"
        })
        self.assertEqual(r_suggest.status_code, 200)
        sug_data = r_suggest.get_json()["data"]

        # 4 & 5. Citizen submits Hindi draft
        hindi_queries = "\n".join([f"{i+1}. {q}" for i, q in enumerate(sug_data["questions"])])
        form_payload = {
            "applicant_name": "सुरेश कुमार वर्मा",
            "applicant_address": "मकान नं. 45, गांधी नगर, वार्ड 15, लखनऊ, उत्तर प्रदेश - 226001",
            "phone": "9811223344",
            "public_authority": "लखनऊ नगर निगम",
            "pio_designation": "जन सूचना अधिकारी (जलकल विभाग)",
            "department_address": "त्रिलोकनाथ रोड, लालबाग, लखनऊ",
            "subject": sug_data["subject"],
            "info_requested": hindi_queries,
            "fee_mode": "ipo",
            "fee_details": "78G 123456",
            "delivery_mode": "Speed Post"
        }
        r_preview = self.client.post("/rti/generate", data=form_payload)
        self.assertEqual(r_preview.status_code, 200)
        preview_html = r_preview.data.decode("utf-8")
        self.assertIn("सुरेश कुमार वर्मा", preview_html)
        self.assertIn("सीवर लाइन निर्माण", preview_html)

        # 6. PDF export with Hindi / Unicode names
        from app.routes.rti import build_rti_text
        draft_text = build_rti_text(form_payload)
        r_pdf = self.client.post("/rti/export-pdf", data={
            "draft_text": draft_text,
            "applicant_name": "सुरेश कुमार वर्मा"
        })
        self.assertEqual(r_pdf.status_code, 200)
        self.assertEqual(r_pdf.headers.get("Content-Type"), "application/pdf")
        self.assertTrue(r_pdf.data.startswith(b"%PDF-"))

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_21_edge_case_preamble_and_fenced_json(self, mock_model_class, mock_env):
        """Verify service safely parses JSON when Gemini includes conversational text and code fences."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        # Model output containing conversational preamble and markdown fence
        mock_response.text = (
            "Certainly! Here is the structured RTI information you requested:\n"
            "```json\n"
            "{\n"
            '  "subject": "Information regarding primary school building repair",\n'
            '  "questions": [\n'
            '    "Certified copy of fund allocation",\n'
            '    "Structural safety audit report"\n'
            "  ]\n"
            "}\n"
            "```\n"
            "I hope this helps your RTI application!"
        )
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("Primary school building repair delayed for 1 year")
        self.assertTrue(result["success"])
        self.assertEqual(result["subject"], "Information regarding primary school building repair")
        self.assertEqual(len(result["questions"]), 2)

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_22_edge_case_single_string_question(self, mock_model_class, mock_env):
        """Verify service safely converts a single string question into a list."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "subject": "Enquiry regarding tender allotment",
            "questions": "Certified copy of the lowest bidder comparative statement."
        })
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("Enquiry regarding tender allotment details")
        self.assertTrue(result["success"])
        self.assertEqual(len(result["questions"]), 1)
        self.assertIn("Certified copy", result["questions"][0])

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_23_edge_case_truncated_json_handling(self, mock_model_class, mock_env):
        """Verify service handles truncated / cut-off JSON safely without crashing."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        # Truncated JSON (token limit reached mid-response)
        mock_response.text = '{"subject": "Information regarding flyover", "questions": ["1. Incomplete item'
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("Flyover construction halted for over 6 months")
        self.assertFalse(result["success"])
        self.assertIn("malformed", result["error"].lower())

    @patch("os.environ.get")
    @patch("google.generativeai.GenerativeModel")
    def test_24_edge_case_empty_subject_and_questions(self, mock_model_class, mock_env):
        """Verify service detects when JSON has empty subject and empty question list."""
        mock_env.return_value = "fake-valid-key-xyz"
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({"subject": "", "questions": []})
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        result = generate_rti_questions("General enquiry with no clear points")
        self.assertFalse(result["success"])
        self.assertIn("Could not extract", result["error"])

    def test_25_query_manipulation_logic(self):
        """Verify numbered list query addition and trimming logic behaves predictably."""
        # Initial questions
        queries = ["1. First query", "2. Second query", "3. Third query"]
        textarea_content = "\n".join(queries)

        # Simulate + Add Query
        lines = [l.strip() for l in textarea_content.split("\n") if l.strip()]
        next_num = len(lines) + 1
        new_content = textarea_content + f"\n{next_num}. "
        self.assertEqual(next_num, 4)
        self.assertTrue(new_content.endswith("4. "))

        # Simulate - Remove Last Query
        split_lines = new_content.strip().split("\n")
        split_lines.pop()
        trimmed_content = "\n".join(split_lines)
        self.assertEqual(trimmed_content, textarea_content)

    def test_26_about_page_ui_and_tech_stack(self):
        """Verify About page renders text-based tech stack, tagline, mission, and features cleanly."""
        # 1. English About page
        resp_en = self.client.get("/about")
        self.assertEqual(resp_en.status_code, 200)
        html_en = resp_en.data.decode("utf-8")
        self.assertIn("NyayaSetu: Smart Civic Rights &amp; Action Guidance System", html_en)
        self.assertIn("tech-stack-list", html_en)
        self.assertIn("tech-stack-item", html_en)
        self.assertIn("Python 3.14", html_en)
        self.assertIn("Flask 3", html_en)
        self.assertIn("SQLite 3", html_en)
        self.assertIn("Gemini API", html_en)
        self.assertIn("ReportLab", html_en)
        # Ensure old icon spans are removed
        self.assertNotIn("tech-card__icon", html_en)

        # 2. Hindi About page
        resp_hi = self.client.get("/about?lang=hi")
        self.assertEqual(resp_hi.status_code, 200)
        html_hi = resp_hi.data.decode("utf-8")
        self.assertIn("हमारे बारे में", html_hi)
        self.assertIn("हमारा मिशन और उद्देश्य", html_hi)
        self.assertIn("प्रौद्योगिकी स्टैक", html_hi)
        self.assertIn("बैकएंड व फ्रेमवर्क", html_hi)


if __name__ == "__main__":
    unittest.main()



