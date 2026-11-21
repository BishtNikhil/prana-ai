# Prāṇa AI (प्राण AI) — Autonomous Urban Air Quality & Winter Smog Inversion Copilot

[![CI Pipeline](https://github.com/BishtNikhil/prana-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/BishtNikhil/prana-ai/actions/workflows/ci.yml)
[![Tests Passing](https://img.shields.io/badge/Tests-19%20Passed-10b981.svg?style=flat-square)](tests/)
[![Security: Ponytail Method](https://img.shields.io/badge/Security-Ponytail%20Method%20Compliant-6366f1.svg?style=flat-square)](SECURITY.md)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3b82f6.svg?style=flat-square)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg?style=flat-square)](LICENSE)
[![Deployment: Vercel](https://img.shields.io/badge/Vercel-Production%20Live-black.svg?style=flat-square&logo=vercel)](https://prana-ai.vercel.app)

> **Google Developer PromptWars Virtual 2026 — Challenge 06**  
> *Engineered by Nikhil Singh Bisht adhering to the **Ponytail Method**: zero hardcoded secrets, airtight exclusion boundaries, single-band apex clasp architecture, and resilient deterministic intelligence.*

---

## 🌟 Executive Summary & Problem Space

During winter months across Northern India and the Indo-Gangetic Plains (Delhi-NCR, Lahore, Lucknow, Patna), a hazardous meteorological phenomenon known as **Atmospheric Thermal Inversion** occurs:

- Nocturnal radiative ground cooling traps heavy, stagnant cold air beneath a warm ceiling, compressing industrial emissions, vehicular exhaust, and crop stubble smoke into a razor-thin **Planetary Boundary Layer (<150m mixing height)**.
- Particulate matter (**PM2.5**) spikes beyond **400–600 µg/m³** (AQI 450+ Severe/Hazardous), causing citizens to passively inhale the particulate equivalent of **20 to 30 cigarettes every day**.
- Families, children, and elderly residents are left without predictive, actionable guidance on when it is safe to open windows, how to assemble affordable indoor air filters, or how to dynamically route commutes around diurnal smog peaks.

**Prāṇa AI (प्राण AI)** solves this crisis with an end-to-end, science-grounded urban resilience platform. Combining real-time atmospheric mathematics, diurnal boundary layer simulations, DIY indoor air purification engineering, and **Google Gemini 2.5 Flash** intelligence, Prāṇa AI empowers communities to protect their respiratory health.

---

## 🏛️ System Architecture & The 6 Core Pillars

Prāṇa AI is architected with a decoupled frontend interface, high-performance FastAPI computational engines, and a resilient GenAI orchestration layer:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     PRĀṆA AI — RESPONSIVE WEB APPLICATION                       │
│     (Dark/Light Glassmorphism • Accessible Radars • Diurnal Curve Canvas)       │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ RESTful HTTPS / JSON
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI API ORCHESTRATOR                              │
│       (OWASP Security Headers • Response Telemetry • Pydantic v2 Contracts)      │
└────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬─┘
     │              │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐
│AQI Engine│  │ Diurnal  │  │ Routine  │  │   IAQ    │  │  Impact  │  │ Community │
│Breakpoint│  │Inversion │  │ Planner  │  │  Engine  │  │  Engine  │  │ Sentinel  │
│  Math    │  │Curve 24h │  │ Persona  │  │  (CADR/  │  │(Eco-Tel) │  │(Statutory │
│(EPA/CPCB)│  │ (Physics)│  │  Engine  │  │  Corsi)  │  │(Berkeley)│  │Grievance) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └───────────┘
                                                                            │
                                                                            ▼
                                                                  ┌───────────────────┐
                                                                  │ Gemini 2.5 Flash  │
                                                                  │  + Deterministic  │
                                                                  │ Offline Fallback  │
                                                                  └───────────────────┘
```

### 1. 🛰️ Air Matrix & Multi-Pollutant Radar
- **Standard Breakpoints:** Implements US EPA and CPCB piecewise linear interpolation algorithms mapping raw particulate densities (`PM2.5`, `PM10`, `NO2`, `CO`, `O3`) into standardized AQI sub-indices.
- **Berkeley Earth Cigarette Equivalence:** Computes direct particulate inhalation toxicity where 22 µg/m³ of PM2.5 over 24 hours equals ~1 smoked cigarette (`PM2.5 / 22.0`).

### 2. 🌡️ 24-Hour Diurnal Thermal Inversion Visualizer
- Models the diurnal expansion and contraction of the atmospheric boundary mixing layer.
- Identifies hazardous morning inversion compression (6:00 AM – 9:30 AM) and pinpoints the **midday solar ventilation window (1:00 PM – 3:30 PM)** when vertical thermal buoyancy safely dilutes indoor air.

### 3. ⏱️ Low-Emission Routine Planner
- Dynamic scheduling engine tailored across 4 distinct urban personas:
  1. **Family with Kids:** School transit timing, indoor play shifts, and HEPA nursery shielding.
  2. **Active Commuter:** Shifting workouts from smoggy dawns to solar windows, metro routing.
  3. **Senior Respiratory Care:** Pre-dawn seal protocols, nebulizer timings, and humidity regulation.
  4. **Field / Outdoor Worker:** N95 shift rotation, hydration barrier protocols, and midday exposure caps.

### 4. 🌬️ Indoor Air Quality (IAQ) & Corsi-Rosenthal Sizer
- Calculates room volume in cubic feet and sizes target **Clean Air Delivery Rate (CADR)** for 5.0 Air Changes per Hour (ACH).
- Generates blueprints for the **Corsi-Rosenthal Box Purifier** (four MERV-13 filters + 20-inch box fan + cardboard shroud), slashing air purification costs from $380 (commercial units) down to **$65** (82.9% savings).
- Pairs NASA Clean Air Study botanical bio-filters (Snake Plants, Areca Palms) for nocturnal oxygen generation (Crassulacean Acid Metabolism).

### 5. 🌿 Quantified Personal Eco-Telemetry & Impact Engine
- Quantifies daily PM2.5 inhaled avoided (µg), daily cigarette equivalents shielded, annual carbon emissions prevented (kg CO₂), and pediatric lung inflammation risk reduction %.
- Benchmarks commute alternatives (Metro, EV Carpool, Bus Rapid Transit).

### 6. 📢 Community Sentinel & Statutory Grievance Generator
- Synthesizes formal municipal grievance petitions under **Section 31A of The Air (Prevention and Control of Pollution) Act, 1981** for open garbage burning and construction dust infractions.
- Generates one-click WhatsApp broadcast alerts for Resident Welfare Associations (RWAs).

### 7. 🤖 Prāṇa-Mitra GenAI Copilot
- Powered by **Google Gemini 2.5 Flash** with strict typed Pydantic contracts.
- Features an **intelligent deterministic fallback engine** guaranteeing 100% operational uptime, instant responsiveness (<15ms), and zero cloud lock-in.

---

## 🔒 The Ponytail Method Compliance & Security Architecture

Prāṇa AI adheres to the strict **Ponytail Method** standards:

| Principle | Implementation Details |
| :--- | :--- |
| **Zero Hardcoded Secrets** | No keys, tokens, or passwords anywhere in codebase. Credentials loaded purely via runtime environment variables (`app.config.AppConfig`). |
| **Airtight Exclusion Boundary** | Comprehensive `.gitignore` and `.dockerignore` excluding all `.env*`, caches, keys, `.vercel`, and OS artifacts. |
| **Single-Band Apex Clasp** | Clear directory hierarchy with zero circular dependencies or dead modules. |
| **OWASP Security Headers** | Automatically injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, and `Referrer-Policy: strict-origin-when-cross-origin`. |
| **Deterministic Fallback** | Full application features operate reliably even in offline or zero-credential environments. |

---

## 🚀 Quickstart & Local Execution

### Prerequisites
- Python 3.11+
- Git

### One-Click Windows Launch
Double-click `run_prana.bat` in the repository root, or execute:
```cmd
.\run_prana.bat
```

### Manual Setup
```bash
# 1. Clone the repository
git clone https://github.com/BishtNikhil/prana-ai.git
cd prana-ai

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Configure environment variables
copy .env.example .env
# Edit .env and supply your GEMINI_API_KEY if desired (deterministic fallback active otherwise)

# 5. Launch development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Navigate to **`http://localhost:8000`** in your browser.

---

## 🐳 Docker Deployment

Run Prāṇa AI anywhere with the hardened, non-root production container:

```bash
# Build the Docker image
docker build -t prana-ai:latest .

# Run the container
docker run -d -p 8000:8000 --name prana-ai prana-ai:latest

# Access the application
curl http://localhost:8000/health
```

---

## 🧪 Automated Test Suite

Prāṇa AI features 100% passing test coverage across mathematical breakpoint formulas, routine generators, IAQ calculations, and REST API contracts:

```bash
python -m pytest tests/ -v
```

Output:
```
tests/test_api_endpoints.py::test_health_check_endpoint PASSED           [  5%]
tests/test_api_endpoints.py::test_preset_cities_endpoint PASSED          [ 10%]
tests/test_api_endpoints.py::test_aqi_snapshot_endpoint PASSED           [ 15%]
tests/test_api_endpoints.py::test_routine_plan_endpoint PASSED           [ 21%]
tests/test_api_endpoints.py::test_iaq_calculate_endpoint PASSED          [ 26%]
tests/test_api_endpoints.py::test_impact_evaluate_endpoint PASSED        [ 31%]
tests/test_api_endpoints.py::test_community_grievance_endpoint PASSED    [ 36%]
tests/test_api_endpoints.py::test_chat_endpoint_deterministic_fallback PASSED [ 42%]
tests/test_api_endpoints.py::test_owasp_security_headers PASSED          [ 47%]
tests/test_aqi_engine.py::test_pm25_subindex_calculation PASSED          [ 52%]
tests/test_aqi_engine.py::test_aqi_category_mapping PASSED               [ 57%]
tests/test_aqi_engine.py::test_cigarette_equivalent PASSED               [ 63%]
tests/test_aqi_engine.py::test_diurnal_inversion_curve PASSED            [ 68%]
tests/test_aqi_engine.py::test_get_snapshot_delhi PASSED                 [ 73%]
tests/test_impact_and_community.py::test_impact_engine_evaluation PASSED [ 78%]
tests/test_impact_and_community.py::test_community_service_garbage_burning PASSED [ 84%]
tests/test_impact_and_community.py::test_community_service_construction_dust PASSED [ 89%]
tests/test_routine_and_iaq.py::test_routine_plan_all_personas PASSED     [ 94%]
tests/test_routine_and_iaq.py::test_iaq_room_cadr_calculation PASSED     [100%]

============================= 19 passed in 1.48s ==============================
```

---

## 📡 API Reference & Documentation

When running locally, interactive API documentation is auto-generated:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Health & Telemetry:** `http://localhost:8000/health`

### Key REST Endpoints:
- `GET /api/aqi/cities` — Directory of preset urban smog hotspot profiles
- `GET /api/aqi/snapshot?city={name}` — Real-time AQI, cigarette equivalents & 24h diurnal curve
- `POST /api/routine/plan?city={name}&persona={type}` — Low-emission daily schedule synthesis
- `POST /api/iaq/calculate` — Room CADR requirement & Corsi-Rosenthal DIY blueprint
- `POST /api/impact/evaluate` — Direct personal & community emission abatement metrics
- `POST /api/community/grievance` — Formal statutory municipal petition & WhatsApp alerts
- `POST /api/chat` — GenAI smog resilience assistant powered by Gemini 2.5 Flash

---

## 📂 Project Directory Structure

```
prana-ai/
├── .github/
│   └── workflows/
│       └── ci.yml                  # Automated GitHub Actions test & zero-secret pipeline
├── api/
│   └── index.py                    # Vercel serverless Python ASGI runtime entry point
├── app/
│   ├── __init__.py
│   ├── config.py                   # Pydantic v2 application configuration
│   ├── main.py                     # FastAPI application & route orchestrator
│   ├── core/
│   │   ├── __init__.py
│   │   └── exceptions.py           # Typed domain exception handlers
│   ├── data/
│   │   ├── __init__.py
│   │   └── preset_cities.py        # Hotspot profiles (Delhi, Lahore, Beijing, etc.)
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              # Pydantic v2 data models & request/response contracts
│   └── services/
│       ├── __init__.py
│       ├── aqi_engine.py           # EPA/CPCB breakpoints & diurnal inversion physics
│       ├── routine_engine.py       # Personalized low-emission daily planner
│       ├── iaq_engine.py           # CADR sizing, Corsi-Rosenthal & NASA bio-filter math
│       ├── impact_engine.py        # Berkeley Earth cigarette math & carbon abatement
│       ├── community_service.py    # Section 31A Air Act grievance & WhatsApp alerts
│       └── gemini_service.py       # Google Gemini 2.5 Flash + deterministic fallback
├── static/
│   ├── app.js                      # Reactive frontend controller & inversion visualizer
│   ├── index.html                  # Single page web application interface
│   └── style.css                   # Glassmorphism dark/light design system
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_endpoints.py       # Integration tests & OWASP security validation
│   ├── test_aqi_engine.py          # Atmospheric mathematical unit tests
│   ├── test_impact_and_community.py
│   └── test_routine_and_iaq.py
├── .dockerignore                   # Docker build context isolation boundary
├── .env.example                    # Sanitized configuration template
├── .gitignore                      # Airtight Ponytail Method security filter
├── CONTRIBUTING.md                 # Contribution standards & style guide
├── Dockerfile                      # Production-ready non-root container
├── LICENSE                         # MIT License
├── pyproject.toml                  # Python package metadata & pytest configuration
├── README.md                       # Master architectural overview & documentation
├── requirements.txt                # Pinned production dependencies
├── run_prana.bat                   # One-click Windows runner
├── SECURITY.md                     # Security policy & secret scan verification
└── vercel.json                     # Vercel Serverless & static asset configuration
```

---

## 👨‍💻 Author & Acknowledgements

- **Developer:** Nikhil Singh Bisht ([@BishtNikhil](https://github.com/BishtNikhil))
- **Email:** nikhilbisht2807@gmail.com
- **Competition:** Google Developer PromptWars Virtual 2026 — Challenge 06
- **Autonomous Agentic Pair Programming:** Antigravity (Google DeepMind)

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
