import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from google import genai
from google.genai import types  
import re
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL_NAME')
client = genai.Client(api_key=GEMINI_API_KEY)

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

        if You dont have the exact data can u just else give me the past data and predict the curent status of the disease and give me the values accordinlgy.


    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(response)
        data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        # 🔥 Clean Gemini response (remove code fences if present)
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]  # take content inside
        cleaned = cleaned.replace("json", "").strip()

        # Parse JSON safely
        diseases = json.loads(cleaned)      

        return JsonResponse({"top_diseases": diseases}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e), "raw": data}, status=500)
    
@csrf_exempt
def top_outbreaks(request):
    client = genai.Client(api_key=GEMINI_API_KEY)
    

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    prompt = '''Please return a JSON array of the top 10 recent verified health news stories focused on disease outbreaks. Each entry should be an object with the following fields:

        - "headline": (string) — the title of the news article.
        - "summary": (string) — a concise summary of the news content.
        - "affected_week": (integer or null) — the number of confirmed affected cases in the entire week, or a hypothetical number if unavailable.
        - "affected_month": (integer or null) — the number of confirmed affected cases in the entire month, or a hypothetical number if unavailable.
        - "affected_year": (integer or null) — the number of confirmed affected cases in the entire year, or a hypothetical number if unavailable.
        - "cured_week": (integer or null) — the number of confirmed cured/recovered cases in the entire week, or a hypothetical number if unavailable.
        - "cured_month": (integer or null) — the number of confirmed cured/recovered cases in the entire month, or a hypothetical number if unavailable.
        - "cured_year": (integer or null) — the number of confirmed cured/recovered cases in the entire year, or a hypothetical number if unavailable.
        - "threat_level": (string) — one of "Low", "Moderate", or "High", based on severity (e.g., number of deaths, transmissibility, public concern).

    Return exactly 10 items. Ensure all values are properly typed, and where data isn't available, use null. Return ONLY valid JSON. Do not include any explanation or commentary.
    '''

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        content = response.text.strip()

        def extract_json_from_response(response_text):
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                raise ValueError("No JSON array found in Gemini response.")

        data = extract_json_from_response(content)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def top_meds(request):
    client = genai.Client(api_key=GEMINI_API_KEY)

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    prompt = '''Please return a JSON array of the top 10 recent verified health news stories focused on latest medical innovation and releases. Each entry should be an object with the following fields:

        - "headline": (string) — the title of the news article.
        - "summary": (string) — a concise summary of the news content.

    Return exactly 10 items. Ensure all values are properly typed, and where data isn't available, use null. Return ONLY valid JSON. Do not include any explanation or commentary.
    '''

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config,
        )

        content = response.text.strip()

        def extract_json_from_response(response_text):
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                raise ValueError("No JSON array found in Gemini response.")

        data = extract_json_from_response(content)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
