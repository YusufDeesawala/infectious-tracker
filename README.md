# 🦠 Infectious Tracker Backend

**Infectious Tracker Backend** is a Django-based API project designed to create **AI-powered health intelligence agents**. These agents use **Google Gemini** (Generative AI) to fetch and process real-time information about **infectious diseases** and outbreaks worldwide.

This backend provides structured **JSON responses** that can be consumed by dashboards, mobile apps, or research tools.

Backend Deployed link = https://infectious-tracker-backend.onrender.com

---

## 🚀 Features

* Built with **Django REST style endpoints**
* Agents powered by **Google Gemini API**
* Real-time outbreak monitoring (using news + health org references)
* JSON-first responses (easy integration with apps & frontend)
* Scalable: more agents can be added for different disease/health tasks

---

## 🧩 Current Agents

### 1. 🌍 **Top Infectious Diseases Agent**

**Endpoint:**

```
POST /api/top-diseases/
```

**What it does:**

* Fetches the **top 3 currently spreading diseases worldwide**.
* Uses Gemini to search & summarize global outbreak news and health data.
* Returns structured JSON with:

  * **name** → disease name
  * **location** → primary affected region(s)
  * **cases** → estimated number of affected people
  * **reference\_url** → trusted source link (WHO, CDC, AP, etc.)

**Response Template:**

```json
{
  "top_diseases": [
    {
      "name": "Disease Name",
      "location": "Primary affected regions",
      "cases": "Estimated cases (with timeframe)",
      "reference_url": "Trusted source URL"
    },
    ...
  ]
}
```

**Example Response:**

```json
{
  "top_diseases": [
    {
      "name": "Dengue",
      "location": "Americas, Asia, Africa",
      "cases": "Over 1.8 million suspected cases reported as of 2024",
      "reference_url": "https://www.paho.org/en/documents/epidemiological-update-dengue-23-february-2024"
    },
    {
      "name": "Cholera",
      "location": "Africa and Asia",
      "cases": "Over 700,000 reported cases globally in 2023",
      "reference_url": "https://www.who.int/emergencies/disease-outbreak-news/item/2024-DON504"
    },
    {
      "name": "Measles",
      "location": "Africa, Asia, Europe",
      "cases": "Over 306,000 reported cases globally in 2023",
      "reference_url": "https://www.who.int/news/item/20-02-2024-measles-cases-continue-to-surge-globally--putting-millions-of-children-at-risk"
    }
  ]
}
```

---

## ⚡ How to Access

### 1. Run Django Server

```bash
python manage.py runserver
```

### 2. Test with Postman / cURL

**Request:**

* Method: `POST`
* URL: `http://127.0.0.1:8000/api/top-diseases/`
* Headers:

  * `Content-Type: application/json`
* Body: *(leave empty)*

**Response:** JSON with the top 3 diseases (see example above).

---

## 🔑 Configuration

* **Gemini API Key**:
  Set your Gemini API key in the project (usually via `settings.py` or environment variables).

  ```bash
  export GEMINI_API_KEY="your_api_key_here"
  ```

* **Model Used**:
  Currently uses `gemini-2.5-flash` (can be upgraded to `gemini-pro` or `gemini-2.5-flash`).

