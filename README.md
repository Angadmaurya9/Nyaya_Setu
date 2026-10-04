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

## ✨ Features (Phase 1 & Phase 2)

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
├── tests_phase2.py          # Automated test suite (7 comprehensive test cases)
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
│   │   └── contact.py       # Contact route: /contact (GET & POST)
│   │
│   ├── static/              # Static assets
│   │   ├── css/
│   │   │   └── main.css     # CSS Custom Properties, Dark/Light theme, Guidance Dashboard styles
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

Run the automated test suite with standard Python `unittest`:

```bash
python tests_phase2.py
```

### Test Suite Coverage:
1. `test_01_knowledge_base_seeding`: Asserts that all 8 categories, verified citations, action steps, and 8 helplines are present in the database.
2. `test_02_classification_engine`: Tests classification against 11 test cases in both English and Hindi.
3. `test_03_problem_to_action_post_flow`: Verifies form submission, 302 redirection, and dashboard rendering.
4. `test_04_privacy_guarantee`: Proves that sensitive raw user text is never saved in the database.
5. `test_05_scope_correction_schemes_redirect`: Tests that out-of-scope `/schemes` URL redirects to `/issue`.
6. `test_06_direct_guidance_routes`: Verifies all 8 guidance routes load in both Hindi and English (16 test points).
7. `test_07_core_informational_routes`: Tests all primary informational and legal pages.

---

## 🎯 Viva & Evaluation Talking Points (for BCA Students)

1. **Why Flask Application Factory?**  
   Enables creating application instances with different configurations (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`) cleanly without global side-effects.
2. **Why constrained Gemini API prompting?**  
   Unconstrained LLMs are prone to hallucinating inaccurate legal advice, which creates serious liability risks. NyayaSetu uses Gemini **only for classification** (returning a strict category slug), while all legal guidance, statutory citations, and procedural remedies come from verified, human-vetted statutory records.
3. **How does Privacy-by-Design work?**  
   The application processes user text in memory, derives the classification slug, and writes only the slug to the database. Even in the event of a database compromise, no citizen's personal problem description is exposed.
4. **Why No Heavy Front-end Frameworks?**  
   Pure CSS custom properties and lightweight vanilla JavaScript provide near-instant load times, zero build steps, and maximum accessibility on low-bandwidth mobile networks across India.

---

## 🗺️ Roadmap: Phase 3 (Future Scope)

The following items are planned for Phase 3:
- Offline / PWA support with localized offline first-aid legal checklists.
- PDF procedural action guide generation (downloadable checklist for printing).
- State-specific police and DLSA jurisdiction locator.
- Direct voice input for citizens who cannot read or write.

---

## 📄 License & Attribution

Developed as a BCA mini-project for educational and civic awareness purposes. Grounded in publicly available statutes and portals of the Government of India.
