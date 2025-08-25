# 🦠 Infectious Tracker

**Infectious Tracker** is a full-stack Django application that combines:

* **Frontend (Django Templates)** → Interactive UI for viewing data
* **Agents (Django API Endpoints)** → Powered by **Google Gemini AI** to fetch, analyze, and predict infectious disease trends

The system provides structured **JSON responses** for API consumers as well as a **built-in frontend** for human-readable reports.

🔗 **Backend Deployed Link:** [https://infectious-tracker-backend.onrender.com](https://infectious-tracker-backend.onrender.com)

---

## 🚀 Features

* **Django-powered full-stack app** (API + frontend in one project)
* **Agents using Google Gemini AI** with optional Google Search grounding
* **Real-time and predictive insights** about diseases, outbreaks, and medical news
* **Frontend templates** for visualization + **JSON API** for integration
* **Scalable architecture** → more agents can be added easily

---

## 🧩 Current Agents (Working Endpoints)

### 1. 🌍 **Top Infectious Diseases Agent**

**Endpoint:**

```
POST /api/top-diseases/
```

**What it does:**

* Returns the **top 3 currently spreading diseases worldwide**
* If live data isn’t available, predicts current status from past outbreak trends
* Returns structured JSON with cases, cured numbers, and trusted references

**Response Example:**

```json
{
  "top_diseases": [
    {
      "name": "Dengue",
      "location": "Americas, Asia, Africa",
      "weekly_cases": 18000,
      "monthly_cases": 72000,
      "yearly_cases": 650000,
      "weekly_cured": 16000,
      "monthly_cured": 68000,
      "yearly_cured": 600000,
      "reference_url": "https://www.who.int/news/item/dengue-update"
    }
  ]
}
```

---

### 2. 📰 **Top Outbreaks Agent**

**Endpoint:**

```
POST /api/top-outbreaks/
```

**What it does:**

* Fetches the **top 10 verified health news stories on recent outbreaks**
* Uses **Gemini + Google Search grounding** for accuracy
* Provides case numbers, cured counts, and a **threat level rating**

**Response Example:**

```json
[
  {
    "headline": "Cholera outbreak in Southern Africa",
    "summary": "Cholera cases are rising in Mozambique and Malawi with WHO monitoring closely.",
    "affected_week": 1200,
    "affected_month": 5400,
    "affected_year": 40000,
    "cured_week": 800,
    "cured_month": 4000,
    "cured_year": 35000,
    "threat_level": "High"
  }
]
```

---

### 3. 💊 **Top Medical Innovations Agent**

**Endpoint:**

```
POST /api/top-meds/
```

**What it does:**

* Returns the **top 10 recent verified news stories** on **medical innovations and new drug releases**
* Provides headline and short summary only (lightweight format)

**Response Example:**

```json
[
  {
    "headline": "WHO approves new Malaria vaccine",
    "summary": "The WHO has approved a groundbreaking malaria vaccine expected to save millions of lives annually."
  }
]
```

---

## ⚡ How to Access

### 1. Run the App Locally

```bash
python manage.py runserver
```

### 2. Test Endpoints (Postman / cURL)

#### Fetch Top Diseases

```bash
curl -X POST http://127.0.0.1:8000/api/top-diseases/ \
     -H "Content-Type: application/json"
```

#### Fetch Top Outbreaks

```bash
curl -X POST http://127.0.0.1:8000/api/top-outbreaks/ \
     -H "Content-Type: application/json"
```

#### Fetch Top Medical Innovations

```bash
curl -X POST http://127.0.0.1:8000/api/top-meds/ \
     -H "Content-Type: application/json"
```

---

## 🔑 Configuration

* **Environment Variables** (stored in `.env` or `.env.example`):

  ```bash
  GEMINI_API_KEY=your_api_key_here
  GEMINI_MODEL_NAME=gemini-2.5-flash
  ```

* **Dependencies:** Installed via `requirements.txt`

  ```bash
  pip install -r requirements.txt
  ```

* **Database:** Uses `db.sqlite3` (default Django setup)

---

## 📂 Project Structure

```
InfectiousTracker/
│── manage.py
│── requirements.txt
│── db.sqlite3
│── .env.example
│── templates/ # Frontend (Django Templates)
│── Agents/  # App + Agent Integration
│── InfectiousTrackerBackend/ # Settings 
│── README.md
```