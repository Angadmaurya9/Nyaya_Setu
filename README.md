# NyayaSetu ⚖️

> **Bridging Citizens and Justice** | नागरिकों और न्याय के बीच सेतु

NyayaSetu is a bilingual (Hindi/English) web platform that helps Indian citizens navigate the legal system. It provides access to general legal information, government welfare schemes, legal-aid resources, and a guided issue-description workflow — completely free of charge.

> ⚠️ **Disclaimer:** NyayaSetu provides general legal information only. This is **not** legal advice and does not create a lawyer–client relationship. Always consult a qualified advocate for your specific situation.

---

## ✨ Features (Phase 1)

| Feature | Status |
|---------|--------|
| Responsive homepage with hero, stats, features | ✅ Done |
| About, Resources, Schemes, Issue, Contact pages | ✅ Done |
| Light / Dark theme (persisted in localStorage) | ✅ Done |
| Hindi / English language selector | ✅ Done |
| Mobile-responsive hamburger navigation | ✅ Done |
| Contact form with server-side validation | ✅ Done |
| Legal pages: Disclaimer, Privacy Policy, Terms | ✅ Done |
| SQLite database foundation (SQLAlchemy ORM) | ✅ Done |
| Modular Flask Blueprints (main, legal, contact) | ✅ Done |
| Environment variable configuration | ✅ Done |
| Accessibility: skip links, ARIA, focus styles | ✅ Done |
| AI-powered legal issue analysis | 🔜 Phase 2 |
| Scheme eligibility checker | 🔜 Phase 2 |
| User authentication & case history | 🔜 Phase 2 |
| Full Gemini API integration | 🔜 Phase 2 |

---

## 🏗️ Project Structure

```
NyayaSetu/
│
├── run.py                   # Development server entry point
├── wsgi.py                  # Production WSGI entry point (Gunicorn)
├── config.py                # Configuration classes (Dev / Prod / Test)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
│
├── app/                     # Flask application package
│   ├── __init__.py          # Application factory (create_app)
│   ├── models.py            # SQLAlchemy ORM models
│   ├── utils.py             # Helpers: language, validation, Jinja2 filters
│   │
│   ├── routes/              # Blueprint route modules
│   │   ├── __init__.py
│   │   ├── main.py          # /, /about, /resources, /schemes, /issue
│   │   ├── legal.py         # /legal/disclaimer, /privacy, /terms
│   │   └── contact.py       # /contact (GET + POST)
│   │
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Master layout (navbar, footer, flash msgs)
│   │   ├── main/
│   │   │   ├── index.html   # Homepage
│   │   │   ├── about.html
│   │   │   ├── resources.html
│   │   │   ├── schemes.html
│   │   │   ├── issue.html   # Issue description form
│   │   │   └── contact.html
│   │   └── legal/
│   │       ├── disclaimer.html
│   │       ├── privacy.html
│   │       └── terms.html
│   │
│   └── static/
│       ├── css/
│       │   └── main.css     # All styles (CSS custom properties + dark theme)
│       └── js/
│           └── main.js      # Theme toggle, nav, flash dismiss (vanilla JS)
│
└── instance/                # Created automatically by Flask
    └── nyayasetu.db         # SQLite database (git-ignored)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.14 |
| Web Framework | Flask 3.1 |
| Database ORM | SQLAlchemy 2.x via Flask-SQLAlchemy 3.1 |
| Database | SQLite (development) |
| Templates | Jinja2 |
| Styling | Pure CSS with Custom Properties (no framework) |
| JavaScript | Vanilla JS (no framework) |
| Fonts | Google Fonts: Poppins + Noto Sans Devanagari |
| Config | python-dotenv |
| AI (Phase 2) | Google Gemini API |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/NyayaSetu.git
cd NyayaSetu
```

### 2. Create and activate a virtual environment

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

```bash
# Copy the example file
copy .env.example .env       # Windows
cp .env.example .env         # macOS / Linux

# Edit .env and set SECRET_KEY to a strong random string:
# python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the development server

```bash
python run.py
```

Visit **http://localhost:5000** in your browser.

---

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | **Yes** | Flask session signing key. Use a long random string in production. |
| `FLASK_ENV` | No | `development` (default) or `production` |
| `FLASK_DEBUG` | No | `1` for dev, `0` for production |
| `DATABASE_URL` | No | SQLAlchemy DB URI. Defaults to `sqlite:///nyayasetu.db` |
| `GEMINI_API_KEY` | Phase 2 | Google Gemini API key — not used in Phase 1 |

> ⚠️ **Never** commit your `.env` file. It is listed in `.gitignore`.

---

## 🔬 Running Tests

Basic startup and route validation (no external test framework needed):

```bash
python -c "
from app import create_app
from config import DevelopmentConfig
app = create_app(DevelopmentConfig)
client = app.test_client()
routes = ['/', '/about', '/resources', '/schemes', '/issue', '/contact',
          '/legal/disclaimer', '/legal/privacy', '/legal/terms']
for r in routes:
    resp = client.get(r)
    print(f'{resp.status_code}  {r}')
"
```

---

## 🚀 Production Deployment (Gunicorn)

```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
gunicorn wsgi:app --workers 4 --bind 0.0.0.0:8000
```

---

## 🗺️ Roadmap

### Phase 1 (Current) ✅
- Flask foundation with Blueprints
- Responsive bilingual UI
- Static legal resources and government schemes
- SQLite database foundation

### Phase 2 (Planned)
- Gemini API integration for legal issue analysis
- Dynamic scheme eligibility checking
- User authentication and case history
- Database-backed scheme and resource management
- PWA / offline support

---

## 🔒 Privacy

NyayaSetu is designed with privacy by default:
- **No** user issue descriptions are stored in Phase 1.
- **No** IP addresses are logged.
- **No** third-party tracking cookies.
- Only anonymous page-path visits are recorded for analytics.

See [Privacy Policy](/legal/privacy) for full details.

---

## 📄 License

This project is for **educational purposes** (BCA student project). No commercial license is granted.

---

## 👨‍💻 Author

Developed as a BCA final project. For questions, use the [contact form](http://localhost:5000/contact).
