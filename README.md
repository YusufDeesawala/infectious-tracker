# 🦠 Infectious Tracker Backend

**Infectious Tracker Backend** is a Django-based API project designed to create **AI-powered health intelligence agents**.
These agents use **Google Gemini** (Generative AI) to fetch, predict, and process real-time information about **infectious diseases**, **outbreaks**, and **medical innovations** worldwide.

This backend provides structured **JSON responses** that can be consumed by dashboards, mobile apps, or research tools.

🔗 **Deployed Link:** [https://infectious-tracker-backend.onrender.com](https://infectious-tracker-backend.onrender.com)

---

## 🚀 Features

* Built with **Django REST-style endpoints**
* Agents powered by **Google Gemini API**
* Real-time outbreak monitoring with **Google Search grounding**
* JSON-first responses (easy integration with apps & frontend)
* Scalable: more agents can be added for different disease/health tasks

---

## 🧩 Current Agents (Endpoints)

### 1. 🌍 **Top Infectious Diseases Agent**

**Endpoint:**

```
POST /api/top-diseases/
```

**What it does:**

* Fetches the **top 3 currently spreading diseases worldwide**.
* If current data isn’t available, predicts trends using past outbreak data.
* Returns structured JSON with:

  * `name` → disease name
  * `location` → primary affected region(s)
  * `weekly_cases` / `monthly_cases` / `yearly_cases`
  * `weekly_cured` / `monthly_cured` / `yearly_cured`
  * `reference_url` → trusted source link (WHO, CDC, AP, etc.)

**Response Template:**

```json
{
  "top_diseases": [
    {
      "name": "Disease Name",
      "location": "Primary affected region(s)",
      "weekly_cases": 100,
      "monthly_cases": 400,
      "yearly_cases": 1500,
      "weekly_cured": 80,
      "monthly_cured": 350,
      "yearly_cured": 1200,
      "reference_url": "https://trustedsource.org/example"
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

* Fetches the **top 10 recent verified health news stories** focused on disease outbreaks.
* Uses **Gemini with Google Search grounding** for reliable information.
* Returns structured JSON with:

  * `headline` → news title
  * `summary` → short article summary
  * `affected_week` / `affected_month` / `affected_year` (numbers or null if unavailable)
  * `cured_week` / `cured_month` / `cured_year` (numbers or null if unavailable)
  * `threat_level` → `"Low" | "Moderate" | "High"`

**Response Template:**

```json
[
  {
    "headline": "Outbreak of Dengue in South America",
    "summary": "Health authorities report rising dengue cases across Brazil and Argentina.",
    "affected_week": 1200,
    "affected_month": 5600,
    "affected_year": 72000,
    "cured_week": 800,
    "cured_month": 4200,
    "cured_year": 65000,
    "threat_level": "Moderate"
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

* Fetches the **top 10 recent verified health news stories** focused on **medical innovations and drug releases**.
* Returns structured JSON with:

  * `headline` → news title
  * `summary` → short article summary

**Response Template:**

```json
[
  {
    "headline": "New Malaria Vaccine Approved by WHO",
    "summary": "The WHO has approved a groundbreaking malaria vaccine expected to save millions of lives annually."
  }
]
```

---

## ⚡ How to Access

### 1. Run Django Server

```bash
python manage.py runserver
```

### 2. Test with Postman / cURL

#### Example: Fetch Top Diseases

```bash
curl -X POST http://127.0.0.1:8000/api/top-diseases/ \
     -H "Content-Type: application/json"
```

#### Example: Fetch Top Outbreaks

```bash
curl -X POST http://127.0.0.1:8000/api/top-outbreaks/ \
     -H "Content-Type: application/json"
```

#### Example: Fetch Top Medical Innovations

```bash
curl -X POST http://127.0.0.1:8000/api/top-meds/ \
     -H "Content-Type: application/json"
```

---

## 🔑 Configuration

* **Gemini API Key**
  Set your Gemini API key in `.env` file:

  ```bash
  GEMINI_API_KEY=your_api_key_here
  GEMINI_MODEL_NAME=gemini-2.5-flash
  ```

* **Environment Variables** are loaded via `python-dotenv`.

* **Model Used**:
  Currently defaults to `gemini-2.5-flash`, but you can upgrade to `gemini-pro` or newer versions.
