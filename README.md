# NyayaSetu ⚖️ (न्यायसेतु)

> **Bridging Citizens and Justice** | नागरिकों और न्याय के बीच सेतु  
> A Privacy-First, Bilingual Problem-to-Action Legal Guidance Platform for Indian Citizens.

NyayaSetu is a web application designed to help everyday citizens navigate the Indian legal system. By translating everyday problem descriptions into structured statutory categories, NyayaSetu empowers users with concrete preliminary action steps, official government portal links, and emergency helplines — completely free, privacy-first, and without confusing legal jargon.

> ⚠️ **Statutory Disclaimer:** NyayaSetu provides general procedural and statutory information only. It is **not** a law firm, does not provide legal representation, and does not create an advocate–client relationship. Always consult a licensed advocate or your District Legal Services Authority (NALSA helpline: 15100) for specific legal matters.

---

## 📌 Problem-to-Action Guidance Flow

```
[ Citizen describes issue in everyday Hindi or English ]
                       │
                       ▼
        [ Gemini 1.5 Flash Classifier ]
        (Strict prompt: slug only, no advice)
                       │
             ┌─────────┴─────────┐
      [ Success ]          [ Fallback / No Key ]
             │                   │
             └─────────┬─────────┘
                       ▼
      [ Match to Verified Category ]
    (Consumer, Tenancy, Family, Labour, etc.)
                       │
                       ▼
      [ Anonymized Query Metric Logged ]
    (Category slug only — raw text NEVER stored)
                       │
                       ▼
        [ Action Guidance Dashboard ]
   ├── Governing Act / Statutory Provision
   ├── Step-by-Step Initial Action Timeline
   ├── Direct Links to Official Government Portals
   ├── Relevant National / State Helplines
   └── Prominent Legal Disclaimer
```

---

## ✨ Features (Phases 1 through 5)

| Feature | Phase | Status |
|---------|-------|--------|
| Modular Flask Application Factory & Blueprints | Phase 1 | ✅ Completed |
| Responsive Layout with Light/Dark Theme (CSS custom properties) | Phase 1 | ✅ Completed |
| Hindi / English Language Selector with Session Persistence | Phase 1 | ✅ Completed |
| Mobile Hamburger Navigation & Skip-to-Content Accessibility | Phase 1 | ✅ Completed |
| Contact Form with Server-Side Validation | Phase 1 | ✅ Completed |
| Legal Pages: Disclaimer, Privacy Policy, Terms of Use | Phase 1 | ✅ Completed |
| Problem-to-Action Issue Analysis Form (`/issue`) | Phase 2 | ✅ Completed |
| Gemini API AI Issue Classification (`gemini-1.5-flash`) | Phase 2 | ✅ Completed |
| Rule-Based / Keyword Fallback Engine (Zero External Dependency) | Phase 2 | ✅ Completed |
| Verified Statutory Knowledge Base (8 Categories, Action Steps) | Phase 2 | ✅ Completed |
| Verified Helpline Directory (112, 15100, 1915, 1930, 181, etc.) | Phase 2 | ✅ Completed |
| Guidance Dashboard (`/guidance/<slug>`) with Step-by-Step Timeline | Phase 2 | ✅ Completed |
| Strict Privacy Safeguard: Zero User Text Retention | Phase 2 | ✅ Completed |
| Scope Correction: Schemes Discovery Removed & Redirected | Phase 2 | ✅ Completed |
| RTI Application Generator Form (`/rti/`) | Phase 3 | ✅ Completed |
| Statutory Section 6(1) RTI Draft Builder | Phase 3 | ✅ Completed |
| Editable RTI Draft Preview & Copy Interface | Phase 3 | ✅ Completed |
| ReportLab PDF Export (`/rti/export-pdf`) with A4 Page Layout | Phase 3 | ✅ Completed |
| Dedicated Print Styles (`window.print()` Clean Output) | Phase 3 | ✅ Completed |
| Statutory Fee & BPL Exemption Handling (Section 7(5)) | Phase 3 | ✅ Completed |
| Proviso to Section 7(1) Life or Liberty 48-Hour Urgency Clause | Phase 3 | ✅ Completed |
| Security Hardening: XSS escaping, XML sanitization, Header policies | Phase 4 | ✅ Completed |
| Robust Error Handling: Mocked API timeouts, Fallback logging | Phase 4 | ✅ Completed |
| Accessibility Hardening: ARIA attributes, semantic headings, contrast | Phase 4 | ✅ Completed |
| Automated Quality & Regression Suites (25/25 passing tests) | Phase 4 | ✅ Completed |
| Project Defense & Viva Documentation, Deployment & Demonstration Scripts | Phase 5 | ✅ Completed |

---

## 🏛️ Verified Legal Knowledge Base & Sources

All guidance records in NyayaSetu are grounded in official Indian statutory frameworks and verified government portals:

1. **Consumer Rights & Service Deficiency (`consumer`)**
   - *Act:* The Consumer Protection Act, 2019
   - *Official Portal:* National Consumer Helpline ([consumerhelpline.gov.in](https://consumerhelpline.gov.in)) & e-Daakhil ([edaakhil.nic.in](https://edaakhil.nic.in))
   - *Helpline:* **1915**
2. **Property, Tenancy & Land Disputes (`property`)**
   - *Act:* Transfer of Property Act, 1882 & Real Estate (Regulation and Development) Act, 2016 (RERA)
   - *Official Authority:* Ministry of Housing and Urban Affairs & State RERA Portals
3. **Family, Maintenance & Matrimonial Issues (`family`)**
   - *Act:* Family Courts Act, 1984, Section 144 BNSS / Section 125 CrPC, Maintenance of Senior Citizens Act, 2007
   - *Official Authority:* National Legal Services Authority (NALSA) & National Commission for Women
4. **Employment, Wages & Workplace Rights (`labour`)**
   - *Act:* Code on Wages, 2019 & Industrial Disputes Act, 1947
   - *Official Portal:* Ministry of Labour SAMADHAN Portal ([samadhan.labour.gov.in](https://samadhan.labour.gov.in))
   - *Helpline:* **1800-180-1111**
5. **Right to Information (`rti`)**
   - *Act:* Right to Information Act, 2005
   - *Official Portal:* RTI Online ([rtionline.gov.in](https://rtionline.gov.in))
6. **Criminal Incidents, Fraud & Police Procedure (`criminal`)**
   - *Act:* Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) & Information Technology Act, 2000
   - *Official Portal:* National Cyber Crime Reporting Portal ([cybercrime.gov.in](https://cybercrime.gov.in))
   - *Helplines:* **112** (Emergency Police), **1930** (Financial Cyber Fraud)
7. **Domestic Violence & Women Safety (`domestic_violence`)**
   - *Act:* Protection of Women from Domestic Violence Act, 2005 (PWDVA)
   - *Official Authority:* Ministry of Women and Child Development One-Stop Centers (Sakhi)
   - *Helpline:* **181** / **1091**
8. **General Legal Aid & Civic Grievance (`other`)**
   - *Act:* Legal Services Authorities Act, 1987 (Article 39A of the Constitution)
   - *Official Authority:* District Legal Services Authorities (DLSA) / NALSA
   - *Toll-Free Helpline:* **15100**

---

## 🔒 Privacy & Zero-Retention Architecture

NyayaSetu is architected with privacy by default:
- **No User Text Stored:** The user's input text is processed transiently in memory for classification and is **never** committed to the database or written to disk logs.
- **Anonymous Metrics Only:** The `user_queries` table only records the identified category slug (e.g., `"consumer"`), classification method (`"gemini"` or `"keyword"`), language (`"en"` or `"hi"`), and timestamp.
- **No Tracking or Third-Party Ads:** No cookies other than standard Flask session for UI preferences (language).

---

## 🏗️ Project Structure

```
NyayaSetu/
│
├── run.py                   # Development server entry point
├── wsgi.py                  # Production WSGI entry point (Gunicorn)
├── config.py                # Environment configuration (Dev, Prod, Test)
├── requirements.txt         # Dependencies (Flask, SQLAlchemy, python-dotenv, google-generativeai)
├── .env.example             # Environment variable template
├── .gitignore               # Git exclusions (.env, venv, instance/*.db, etc.)
├── tests_phase2.py          # Phase 2 automated test suite (7 tests)
├── tests_phase3.py          # Phase 3 automated test suite (7 tests: RTI & Regression)
├── README.md                # Project documentation
│
├── app/                     # Main application package
│   ├── __init__.py          # Application Factory (create_app), extension init, auto-seeding
│   ├── models.py            # SQLAlchemy models (LegalCategory, LegalGuidance, Helpline, UserQuery, SiteVisit)
│   ├── knowledge_base.py    # Seed data module for verified categories and helplines
│   ├── utils.py             # Helpers (language detection, input validation, Jinja2 filters)
│   │
│   ├── services/            # Service modules
│   │   ├── __init__.py
│   │   └── gemini_service.py # Gemini 1.5 Flash integration + Keyword fallback engine
│   │
│   ├── routes/              # Modular blueprints
│   │   ├── __init__.py
│   │   ├── main.py          # Core routes: /, /about, /resources, /issue, /guidance/<slug>
│   │   ├── legal.py         # Informational routes: /legal/disclaimer, /privacy, /terms
│   │   ├── contact.py       # Contact route: /contact (GET & POST)
│   │   └── rti.py           # Phase 3: RTI Generator (/rti, /rti/generate, /rti/export-pdf)
│   │
│   ├── static/              # Static assets
│   │   ├── css/
│   │   │   └── main.css     # CSS Custom Properties, Dark/Light theme, RTI & print styles
│   │   └── js/
│   │       └── main.js      # Vanilla JS (Theme toggle, hamburger menu, flash dismiss)
│   │
│   └── templates/           # Jinja2 templates
│       ├── base.html        # Master base template
│       ├── main/
│       │   ├── index.html   # Homepage with problem-to-action cards
│       │   ├── about.html   # Mission & architecture overview
│       │   ├── resources.html# Official portals & helplines directory
│       │   ├── issue.html   # Problem description form with character counter
│       │   ├── guidance.html# Action Guidance Dashboard (timeline, citations, helplines)
│       │   └── contact.html # Contact form
│       ├── rti/
│       │   ├── generator.html# RTI Application Generator input form
│       │   └── preview.html # Editable RTI draft preview with PDF download & print
│       └── legal/
│           ├── disclaimer.html
│           ├── privacy.html
│           └── terms.html
│
└── instance/                # Local database folder (git-ignored)
    └── nyayasetu.db         # SQLite database
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/Angadmaurya9/Nyaya_Setu.git
cd NyayaSetu
```

### 2. Set up virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and configure:
```ini
# Flask secret key
SECRET_KEY=generate-a-random-secret-key-here

# Flask environment
FLASK_ENV=development
FLASK_DEBUG=1

# SQLite database path
DATABASE_URL=sqlite:///nyayasetu.db

# Google Gemini API Key (Optional but recommended)
# Get a free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your-gemini-api-key-here
```

> **Note on Gemini API Key:**  
> If `GEMINI_API_KEY` is not provided or quota is exceeded, NyayaSetu **automatically and gracefully falls back** to the built-in rule-based keyword classification engine. All features will continue to work without crashing.

### 5. Run the application
```bash
python run.py
```
Open your browser and visit: **http://127.0.0.1:5000**

---

## 🧪 Testing Instructions

Run the automated test suites using standard Python `unittest`:

```bash
# Run all test suites across Phases 2, 3, and 4 (25 total tests)
python tests_phase2.py
python tests_phase3.py
python tests_phase4.py
```

### Comprehensive Test Coverage (25 Automated Tests):
- **Phase 2 Suite (`tests_phase2.py` - 7 tests):**
  1. Database model & statutory knowledge base seeding (8 categories, 8 helplines).
  2. Gemini classifier & bilingual keyword fallback accuracy (11 test cases in EN & HI).
  3. Problem-to-action POST flow (302 redirect and guidance rendering).
  4. Privacy verification (raw user text is strictly never stored in DB).
  5. Scope correction (/schemes safely redirected to /issue).
  6. Direct bilingual guidance routing (all 8 slugs in EN and HI).
  7. Core informational routes status.

- **Phase 3 Suite (`tests_phase3.py` - 7 tests):**
  1. RTI Generator route accessibility (`/rti/`).
  2. RTI draft builder logic with required statutory sections.
  3. Life & liberty proviso handling (48-hour clause under Section 7(1)).
  4. Statutory fee exemption (BPL status under Section 7(5)).
  5. Form input validation and error handling for missing fields.
  6. ReportLab PDF generation and valid `%PDF` binary output.
  7. Zero-retention privacy for RTI personal details.

- **Phase 4 Suite (`tests_phase4.py` - 11 tests):**
  1. Core application routes & HTTP 200 checks.
  2. Structured guidance retrieval and graceful fallback on invalid slugs.
  3. Knowledge base data integrity and official HTTPS source citations.
  4. Mocked Gemini API timeouts and resilient keyword fallback.
  5. Graceful recovery from mocked AI hallucinated/invalid slugs.
  6. Empty and excessively long input validation (1000 character limit).
  7. XSS, HTML, and script injection sanitization.
  8. Privacy assertion across the complete database state.
  9. Production configuration debug safety check.
  10. PDF generator special character handling (`<`, `>`, `&`, multi-page flow).
  11. Custom 404 error page and user-friendly error recovery.

---

## 🚀 Production Deployment

NyayaSetu is production-ready and includes a standard WSGI entry point (`wsgi.py`):

```bash
# 1. Set production environment variables in .env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-strong-random-secret-key

# 2. Run with Gunicorn WSGI server
gunicorn wsgi:app --workers 4 --bind 0.0.0.0:8000
```

---

## 🎯 Viva & Evaluation Talking Points

1. **Why Flask Application Factory?**  
   Enables creating application instances with different configurations (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`) cleanly without global side-effects.
2. **Why constrained Gemini API prompting?**  
   Unconstrained LLMs are prone to hallucinating inaccurate legal advice, which creates serious liability risks. NyayaSetu uses Gemini **only for classification** (returning a strict category slug), while all legal guidance, statutory citations, and procedural remedies come from verified, human-vetted statutory records.
3. **How does Privacy-by-Design work?**  
   The application processes user text in memory, derives the classification slug, and writes only the slug to the database. Even in the event of a database compromise, no citizen's personal problem description is exposed.
4. **Why No Heavy Front-end Frameworks?**  
   Pure CSS custom properties and lightweight vanilla JavaScript provide near-instant load times, zero build steps, and maximum accessibility on low-bandwidth mobile networks across India.

---

## 🗺️ Future Scope & Scaling

- **PWA & Offline First:** Localized service worker caching of statutory checklists for rural areas without internet.
- **Multilingual Expansion:** Integration with Bhashini AI / IndicTrans to cover all 22 official languages of India.
- **State-Specific Jurisdiction:** Geolocation mapping to district-level DLSA offices and police jurisdictions.
- **Voice Assistance:** Speech-to-text input for citizens with low literacy levels.

---

## 📄 License & Attribution

NyayaSetu: Smart Civic Rights & Action Guidance System is an educational civic-tech initiative grounded in publicly available statutes and portals of the Government of India.
