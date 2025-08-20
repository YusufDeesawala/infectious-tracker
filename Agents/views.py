import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from google import genai
from google.genai import types  
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL_NAME')

@csrf_exempt
def top_diseases(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    prompt = """
    Please respond ONLY with a JSON array of the top 3 diseases currently spreading worldwide. 
    Do not include code fences, explanations, or extra text.
    Each item must have:
    - "name": disease name
    - "location": geographic area
    - "cases": estimated number of people affected
    - "reference_url": source URL
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
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
    
    client = genai.Client(GEMINI_API_KEY)

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    prompt = '''Please return a JSON array of the top 10 recent verified health news stories focused on disease outbreaks. Each entry should be an object with the following fields:

        - "headline": (string) — the title of the news article.
        - "imageurl": (string) — the URL of an image associated with the news (if available, otherwise empty string).
        - "summary": (string) — a concise summary of the news content.
        - "affected_count": (integer or null) — the number of confirmed affected cases, or null if unavailable.
        - "cured_count": (integer or null) — the number of confirmed cured/recovered cases, or null if unavailable.
        - "threat_level": (string) — one of "Low", "Moderate", or "High", based on severity (e.g., number of deaths, transmissibility, public concern).

    Return exactly 10 items. Ensure all values are properly typed, and where data isn't available, use null. Example format:

        [
            {
                "headline": "Example outbreak headline",
                "imageurl": "https://example.com/image.jpg",
                "summary": "Brief summary here...",
                "affected_count": 500,
                "cured_count": 450,
                "threat_level": "Moderate"
            },
            ...
        ]
    '''

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        content = response.text.strip()

        data = json.loads(content)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def top_outbreaks(request):
    
    client = genai.Client(GEMINI_API_KEY)

    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    prompt = '''Please return a JSON array of the top 10 recent verified health news stories focused on disease outbreaks. Each entry should be an object with the following fields:

        - "headline": (string) — the title of the news article.
        - "imageurl": (string) — the URL of an image associated with the news (if available, otherwise empty string).
        - "summary": (string) — a concise summary of the news content.
        - "affected_count": (integer or null) — the number of confirmed affected cases, or null if unavailable.
        - "cured_count": (integer or null) — the number of confirmed cured/recovered cases, or null if unavailable.
        - "threat_level": (string) — one of "Low", "Moderate", or "High", based on severity (e.g., number of deaths, transmissibility, public concern).

    Return exactly 10 items. Ensure all values are properly typed, and where data isn't available, use null. Example format:

        [
            {
                "headline": "Example outbreak headline",
                "imageurl": "https://example.com/image.jpg",
                "summary": "Brief summary here...",
                "affected_count": 500,
                "cured_count": 450,
                "threat_level": "Moderate"
            },
            ...
        ]
    '''

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        content = response.text.strip()

        data = json.loads(content)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

