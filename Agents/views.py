import requests
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from dotenv import load_dotenv
import re
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Load primary and fallback Gemini API keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_KEY_FALLBACK = os.getenv('GEMINI_API_KEY_FALLBACK')
GEMINI_MODEL = os.getenv('GEMINI_MODEL_NAME')  # e.g., 'gemini-1.5-flash'

# Ensure a 'data' directory exists to store JSON files
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def call_gemini_api(prompt, api_key, endpoint):
    """Helper function to call Gemini API with a given API key"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Clean response (remove code fences if present)
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].strip()
        cleaned = cleaned.replace("json", "").strip()
        return json.loads(cleaned)
    except Exception as e:
        logger.error(f"Gemini API call failed for {endpoint} with error: {str(e)}")
        raise

@csrf_exempt
def top_diseases(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    prompt = """
        Please respond ONLY with a JSON array of the top 3 diseases currently spreading worldwide.  
        Each item must have:  
        - "name": disease name  
        - "location": geographic area  
        - "weekly_cases": number of people affected this week (digits only)  
        - "monthly_cases": number of people affected this month (digits only)  
        - "yearly_cases": number of people affected this year (digits only)  
        - "weekly_cured": number of people cured this week (digits only)  
        - "monthly_cured": number of people cured this month (digits only)  
        - "yearly_cured": number of people cured this year (digits only)  
        - "reference_url": source URL  

        Do not include code fences, explanations, or extra text.

        If you don't have the exact data, use past data and predict the current status of the disease, providing values accordingly.
    """

    try:
        logger.info("Attempting to fetch top diseases with primary API key")
        diseases = call_gemini_api(prompt, GEMINI_API_KEY, "top_diseases")
    except Exception as e:
        logger.warning(f"Primary API key failed for top_diseases: {str(e)}")
        if GEMINI_API_KEY_FALLBACK:
            logger.info("Retrying with fallback API key")
            try:
                diseases = call_gemini_api(prompt, GEMINI_API_KEY_FALLBACK, "top_diseases")
            except Exception as e2:
                logger.error(f"Fallback API key also failed for top_diseases: {str(e2)}")
                return JsonResponse({"error": f"Both API keys failed: Primary - {str(e)}, Fallback - {str(e2)}"}, status=500)
        else:
            logger.error("No fallback API key configured")
            return JsonResponse({"error": f"No fallback API key available: {str(e)}"}, status=500)

    # Save to diseases.json (overwrite)
    try:
        with open(os.path.join(DATA_DIR, 'diseases.json'), 'w') as f:
            json.dump(diseases, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save diseases.json: {str(e)}")
        return JsonResponse({"error": f"Failed to save data: {str(e)}"}, status=500)

    return JsonResponse({"top_diseases": diseases}, safe=False)

@csrf_exempt
def top_outbreaks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    prompt = """
        Please return a JSON array of the top 10 recent verified health news stories focused on disease outbreaks. Each entry should be an object with the following fields:

        - "headline": (string) — the title of the news article.
        - "summary": (string) — a concise summary of the news content.
        - "affected_week": (integer or null) — the number of confirmed affected cases in the entire week, or a hypothetical number if unavailable.
        - "affected_month": (integer or null) — the number of confirmed affected cases in the entire month, or a hypothetical number if unavailable.
        - "affected_year": (integer or null) — the number of confirmed affected cases in the entire year, or a hypothetical number if unavailable.
        - "cured_week": (integer or null) — the number of confirmed cured/recovered cases in the entire week, or a hypothetical number if unavailable.
        - "cured_month": (integer or null) — the number of confirmed cured/recovered cases in the entire month, or a hypothetical number if unavailable.
        - "cured_year": (integer or null) — the number of confirmed cured/recovered cases in the entire year, or a hypothetical number if unavailable.
        - "threat_level": (string) — one of "Low", "Moderate", or "High", based on severity (e.g., number of deaths, transmissibility, public concern).

        Return exactly 10 items. Ensure all values are properly typed, and where data isn't available, use a hypothetical value. Return ONLY valid JSON. Do not include any explanation or commentary.
    """

    try:
        logger.info("Attempting to fetch top outbreaks with primary API key")
        outbreaks = call_gemini_api(prompt, GEMINI_API_KEY, "top_outbreaks")
    except Exception as e:
        logger.warning(f"Primary API key failed for top_outbreaks: {str(e)}")
        if GEMINI_API_KEY_FALLBACK:
            logger.info("Retrying with fallback API key")
            try:
                outbreaks = call_gemini_api(prompt, GEMINI_API_KEY_FALLBACK, "top_outbreaks")
            except Exception as e2:
                logger.error(f"Fallback API key also failed for top_outbreaks: {str(e2)}")
                return JsonResponse({"error": f"Both API keys failed: Primary - {str(e)}, Fallback - {str(e2)}"}, status=500)
        else:
            logger.error("No fallback API key configured")
            return JsonResponse({"error": f"No fallback API key available: {str(e)}"}, status=500)

    # Save to outbreaks.json (overwrite)
    try:
        with open(os.path.join(DATA_DIR, 'outbreaks.json'), 'w') as f:
            json.dump(outbreaks, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save outbreaks.json: {str(e)}")
        return JsonResponse({"error": f"Failed to save data: {str(e)}"}, status=500)

    return JsonResponse(outbreaks, safe=False)

@csrf_exempt
def top_meds(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    prompt = """
        Please return a JSON array of the top 10 recent verified health news stories focused on latest medical innovation and releases. Each entry should be an object with the following fields:

        - "headline": (string) — the title of the news article.
        - "summary": (string) — a concise summary of the news content.

        Return exactly 10 items. Ensure all values are properly typed, and where data isn't available, use null. Return ONLY valid JSON. Do not include any explanation or commentary.
    """

    try:
        logger.info("Attempting to fetch top medical news with primary API key")
        meds = call_gemini_api(prompt, GEMINI_API_KEY, "top_meds")
    except Exception as e:
        logger.warning(f"Primary API key failed for top_meds: {str(e)}")
        if GEMINI_API_KEY_FALLBACK:
            logger.info("Retrying with fallback API key")
            try:
                meds = call_gemini_api(prompt, GEMINI_API_KEY_FALLBACK, "top_meds")
            except Exception as e2:
                logger.error(f"Fallback API key also failed for top_meds: {str(e2)}")
                return JsonResponse({"error": f"Both API keys failed: Primary - {str(e)}, Fallback - {str(e2)}"}, status=500)
        else:
            logger.error("No fallback API key configured")
            return JsonResponse({"error": f"No fallback API key available: {str(e)}"}, status=500)

    # Save to meds.json (overwrite)
    try:
        with open(os.path.join(DATA_DIR, 'meds.json'), 'w') as f:
            json.dump(meds, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save meds.json: {str(e)}")
        return JsonResponse({"error": f"Failed to save data: {str(e)}"}, status=500)

    return JsonResponse(meds, safe=False)

@csrf_exempt
def rag_chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    try:
        body = json.loads(request.body)
        question = body.get('question')
        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)

        # Load all JSON data
        diseases = []
        outbreaks = []
        meds = []
        try:
            if os.path.exists(os.path.join(DATA_DIR, 'diseases.json')):
                with open(os.path.join(DATA_DIR, 'diseases.json'), 'r') as f:
                    diseases = json.load(f)
            if os.path.exists(os.path.join(DATA_DIR, 'outbreaks.json')):
                with open(os.path.join(DATA_DIR, 'outbreaks.json'), 'r') as f:
                    outbreaks = json.load(f)
            if os.path.exists(os.path.join(DATA_DIR, 'meds.json')):
                with open(os.path.join(DATA_DIR, 'meds.json'), 'r') as f:
                    meds = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON data for chatbot: {str(e)}")
            return JsonResponse({"error": f"Failed to load data: {str(e)}"}, status=500)

        # Combine data into a single context string
        context = {
            "diseases": diseases,
            "outbreaks": outbreaks,
            "meds": meds
        }
        context_str = json.dumps(context, indent=2)

        # RAG Prompt for Gemini
        rag_prompt = f"""
        You are a helpful assistant that answers questions based ONLY on the provided data. Use External knowledge also plus the provided data to answer the question accurately.
        Data: {context_str}

        Question: {question}

        Provide a concise, accurate answer based on the data. If the question cannot be answered from the data, say "I don't have information on that."
        """

        try:
            logger.info("Attempting to fetch chatbot response with primary API key")
            answer = call_gemini_api(rag_prompt, GEMINI_API_KEY, "rag_chatbot")
        except Exception as e:
            logger.warning(f"Primary API key failed for rag_chatbot: {str(e)}")
            if GEMINI_API_KEY_FALLBACK:
                logger.info("Retrying with fallback API key")
                try:
                    answer = call_gemini_api(rag_prompt, GEMINI_API_KEY_FALLBACK, "rag_chatbot")
                except Exception as e2:
                    logger.error(f"Fallback API key also failed for rag_chatbot: {str(e2)}")
                    return JsonResponse({"error": f"Both API keys failed: Primary - {str(e)}, Fallback - {str(e2)}"}, status=500)
            else:
                logger.error("No fallback API key configured")
                return JsonResponse({"error": f"No fallback API key available: {str(e)}"}, status=500)

        return JsonResponse({"answer": answer})

    except Exception as e:
        logger.error(f"Chatbot processing error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def dashboard(request):
    """Render the main dashboard page"""
    return render(request, 'dashboard.html')