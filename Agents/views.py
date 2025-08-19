import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
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