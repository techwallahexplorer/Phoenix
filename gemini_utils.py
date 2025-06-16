import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""
# Updated to the latest Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Utility to list available models for debugging
GEMINI_LIST_MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def list_gemini_models(api_key=None):
    """
    Lists available Gemini models for the current API key.
    """
    import requests
    api_key = api_key or GEMINI_API_KEY
    url = f"{GEMINI_LIST_MODELS_URL}?key={api_key}"
    resp = requests.get(url)
    try:
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return f"Error listing models: {e}\nResponse: {getattr(resp, 'text', '')}"

def gemini_generate_flashcards(text, subject=None, api_key=None):
    api_key = api_key or GEMINI_API_KEY
    if not api_key:
        raise ValueError("Gemini API key not set. Set GEMINI_API_KEY as env variable or pass as argument.")
    prompt = f"""
You are an expert {subject or 'general'} educator. Given the following educational content, generate at least 12 question-answer flashcards, even if the input is very short. If the content is insufficient, create creative or related questions to reach at least 12 flashcards. Each flashcard should have:
- A clear, concise question
- A factually correct, self-contained answer
Format output as Q: ...\nA: ... pairs.\n\nContent:\n{text}
"""
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    url = f"{GEMINI_API_URL}?key={api_key}"
    try:
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        result = resp.json()
        print("FULL GEMINI API RESPONSE:", result, flush=True)  # Debug print
    except requests.exceptions.HTTPError as e:
        # Show detailed error message for debugging
        raise RuntimeError(f"Gemini API error: {e}\nResponse: {getattr(e.response, 'text', '')}")
    except Exception as e:
        raise RuntimeError(f"Error connecting to Gemini API: {e}")

    # Gemini returns output in a nested structure
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raise RuntimeError(f"Unexpected Gemini API response: {result}")
