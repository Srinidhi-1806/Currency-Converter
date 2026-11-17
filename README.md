# Context-Aware Product Value & Personal Affordability Analyzer

> **"Price tells you what a product costs. Context tells you what it means for your budget."**

A complete, production-style, mobile-responsive web application that analyzes the **true purchasing value** and **personal affordability** of any consumer product by uniting optical character recognition (OCR), real-time currency conversion, category-specific purchasing power parity (PPP) adjustments, and personal discretionary cashflow analysis.

---

## 🌟 Core Concept & Workflow

```text
       USER INPUT (Image / Camera / Manual / Sample Presets)
                               |
                               v
                     IMAGE PREPROCESSING
            (Grayscale -> Bilateral Filter -> Otsu Binarization)
                               |
                               v
                          OCR ENGINE
            (Tesseract & Regex Multi-Currency Extraction)
                               |
                     +---------+---------+
                     |                   |
                  PRICE               CURRENCY
                     |                   |
                     +---------+---------+
                               |
                               v
                     PRODUCT IDENTIFICATION
                   & CATEGORY DETECTION (Rule-Based)
                               |
                               v
                 REAL-TIME EXCHANGE RATE API
              (Live Provider with Fallback Caching)
                               |
                               v
                     MARKET CONVERTED PRICE
                               |
                               v
                 CATEGORY-AWARE PPP ADJUSTMENT
               (Local Market Elasticity & Indices)
                               |
                               v
                    EFFECTIVE PRODUCT VALUE
                               |
                               v
                 PERSONAL MONTHLY CASHFLOW
             (Income - Fixed - Variable - Commitments)
                               |
                               v
                    DISPOSABLE MONTHLY BUDGET
                               |
                               v
                       BUDGET IMPACT %
                               |
                               v
                   DETERMINISTIC AFFORDABILITY SCORE
                           (0 - 100 Gauge)
                               |
                               v
                 DECISION & RECOMMENDATION ENGINE
               (BUY / CONSIDER / WAIT / NOT RECOMMENDED)
                               |
                               v
                   INTERACTIVE RESULT DASHBOARD
             (Chart.js Visualizations & Math Breakdown)
```

---

## 🚀 Key Differentiating Innovations

1. **Context-Aware Currency Conversion**: Traditional tools only execute `Price × Rate = Converted`. This platform weaves product context, category elasticity, local economic purchasing power, and personal budget limits into a cohesive financial decision.
2. **Category-Aware Purchasing Power Parity (PPP)**: Electronics, food, groceries, and fashion have distinct local manufacturing, tariff, and retail dynamics. Category-specific factors adjust nominal prices into effective purchasing values.
3. **Personal Budget-Aware Discretionary Impact**: Evaluates product cost against uncommitted disposable surplus (`Income - Fixed - Variable - Commitments`), not just raw income.
4. **Effective Product Value vs. Market Price**: Clearly separates nominal currency conversion from contextual local purchasing value.
5. **Budget-Safe Price Ceiling (20% Threshold)**: Calculates the maximum safe price ceiling for a purchase and provides target budget guidance for unaffordable items.
6. **Deterministic & Explainable Score**: Fully transparent 0–100 score with step-by-step mathematical breakdowns in an interactive accordion.
7. **Purchase Decision Support**: Clear guidance categorized as `BUY`, `CONSIDER`, `WAIT`, or `NOT RECOMMENDED`.

---

## 🛠️ Technology Stack

### Frontend
- **HTML5 & Vanilla CSS3**: Modern glassmorphism, responsive cards, touch-friendly (>44px) controls, dark sapphire theme.
- **Vanilla JavaScript**: Modular architecture (`app.js`, `upload.js`, `ocr.js`, `budget.js`, `charts.js`, `analysis.js`, `history.js`).
- **Chart.js 4.4**:
  - *Chart 1*: Price Transformation Waterfall (Original → Converted → PPP Effective Value)
  - *Chart 2*: Budget Impact Comparison (Product Value vs Disposable vs Safe Limit)
  - *Chart 3*: Monthly Cashflow Post-Purchase Simulation
- **Responsive Layout**: Optimized for 320px, 375px, 390px, 414px, 768px, 1024px, 1440px+.

### Backend
- **Python 3.11+**
- **FastAPI & Uvicorn**: High-performance asynchronous REST API.
- **SQLAlchemy ORM**: Relational models for users, budgets, products, categories, currencies, exchange rates, PPP indices, OCR results, and analyses.
- **Database**: MySQL ready with zero-friction SQLite automatic fallback.
- **OCR & Computer Vision**: OpenCV (`cv2`), Pillow (`PIL`), Tesseract (`pytesseract`), robust regex currency extractors.
- **External API**: Real-time exchange rate engine with database caching and fallback tables.

---

## 📂 Project Structure

```text
Currency converters/
│
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI Application & Static Mounts
│   │   ├── config.py                    # App Configuration & Settings
│   │   │
│   │   ├── api/                         # REST API Routers
│   │   │   ├── routes_ocr.py            # OCR image processing endpoint
│   │   │   ├── routes_currency.py       # Live exchange rate & conversion
│   │   │   ├── routes_ppp.py            # Category PPP & Admin CRUD
│   │   │   ├── routes_budget.py         # Personal monthly budget manager
│   │   │   ├── routes_product.py        # Categories & subcategories
│   │   │   └── routes_analysis.py       # Complete 11-step analysis workflow
│   │   │
│   │   ├── models/                      # SQLAlchemy Relational Models
│   │   │   ├── user.py                  # User profile
│   │   │   ├── budget.py                # Monthly budget cashflow
│   │   │   ├── product.py               # Products, Categories, Currencies, Rates
│   │   │   ├── ppp.py                   # PPP index records
│   │   │   └── analysis.py              # Saved evaluations & OCR metadata
│   │   │
│   │   ├── schemas/                     # Pydantic Validation Schemas
│   │   │   ├── ocr.py
│   │   │   ├── budget.py
│   │   │   ├── product.py
│   │   │   ├── ppp.py
│   │   │   ├── currency.py
│   │   │   └── analysis.py
│   │   │
│   │   ├── services/                    # Business Logic Services
│   │   │   ├── ocr_service.py           # Preprocessing & text parsing
│   │   │   ├── currency_service.py      # Real-time exchange rates & caching
│   │   │   ├── product_service.py       # Subcategory & product inference
│   │   │   ├── ppp_service.py           # PPP calculations & factors
│   │   │   ├── affordability_service.py # Deterministic score & math steps
│   │   │   └── recommendation_service.py# Contextual recommendation generator
│   │   │
│   │   ├── database/                    # Database Engine & Seed Data
│   │   │   ├── connection.py            # DB engine & session management
│   │   │   └── init_db.py               # Seed categories, countries, PPP indices
│   │   │
│   │   └── utils/                       # Calculation & Validation Utilities
│   │       ├── validators.py
│   │       └── calculations.py
│   │
│   ├── uploads/                         # Uploaded product images
│   ├── tests/
│   │   └── test_analyzer.py             # Unit tests for core algorithms
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
│
├── frontend/
│   ├── index.html                       # Landing page & value proposition
│   ├── analyze.html                     # Multi-step analysis wizard studio
│   ├── budget.html                      # Personal monthly budget manager
│   ├── result.html                      # Standalone result & permalink report
│   ├── history.html                     # Filterable analysis history
│   ├── ppp-manager.html                 # Admin / PPP factor configuration studio
│   │
│   ├── css/
│   │   ├── style.css                    # Design tokens, typography & base styles
│   │   ├── components.css               # Step wizard, gauges, cards, accordions
│   │   └── responsive.css               # Mobile-first breakpoints & navigation
│   │
│   └── js/
│       ├── app.js                       # Global state, API client & toasts
│       ├── upload.js                    # Drag & drop, camera & demo presets
│       ├── ocr.js                       # OCR preview & verification bindings
│       ├── budget.js                    # Live budget calculator & donut chart
│       ├── charts.js                    # Chart.js visualization controllers
│       ├── analysis.js                  # Step wizard & dashboard renderer
│       └── history.js                   # History filtering & table management
│
├── test_e2e_suite.py                    # End-to-end integration test runner
└── README.md                            # Documentation
```

---

## ⚡ Quick Start Guide

### 1. Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment (Optional)
The application comes pre-configured with SQLite fallback and free live exchange rates out of the box. If using MySQL, configure `backend/.env`:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/affordability_db
SQLITE_FALLBACK_URL=sqlite:///./affordability.db
EXCHANGE_RATE_API_URL=https://open.er-api.com/v6/latest
```

### 3. Launch Backend & Web Server
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open your browser at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 Verified Demo Scenario (Section 35)

- **User**:
  - Country: **India** (Currency: **INR**)
  - Monthly Income: **₹40,000**
  - Fixed Expenses: **₹18,000** | Variable Expenses: **₹7,000** | Commitments: **₹5,000**
  - **Disposable Monthly Budget: ₹10,000**
- **Product**:
  - Name: **Sony Wireless Headphones**
  - Original Price: **$49.99 USD**
  - Category: **Electronics**
- **Workflow Execution**:
  1. Live USD → INR exchange rate applied (e.g. ~₹96.47) → Converted Price: **₹4,822.41**
  2. Electronics Category PPP factor (**0.82**) applied → Effective Product Value: **₹3,954.38**
  3. Budget Impact: **39.5%** of ₹10,000 disposable cashflow
  4. Safe 20% Budget Ceiling: **₹2,000.00** (Product is ₹1,954.38 above safe threshold)
  5. Affordability Score: **60/100 (Moderate Affordability)**
  6. Decision: **CONSIDER** with personalized guidance and Chart.js visualizations!

---

## 🔒 Academic & Financial Disclaimer
> *Purchasing-power adjustments and affordability scores generated by this system are analytical estimates intended for educational and decision-support purposes. They do not constitute official government PPP measurements or certified financial advice.*
