import os
from google import genai
from google.genai import types
from src.models.flashcard import FlashcardDeck

def generate_flashcards_structured(text: str, subject: str = None, api_key: str = None) -> FlashcardDeck:
    """
    Uses Google GenAI SDK to generate structured flashcards from text.
    Returns a validated Pydantic FlashcardDeck object.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("Gemini API key not set. Please set GEMINI_API_KEY environment variable.")
    
    # Initialize the official GenAI client
    client = genai.Client(api_key=key)
    
    # Determine subject context
    subject_context = subject or "general"
    
    prompt = f"""
    You are an expert {subject_context} educator. 
    Given the following educational content, generate at least 12 question-answer flashcards. 
    If the content is very short or insufficient, create creative or related questions to reach at least 12 flashcards. 
    Each flashcard should have:
    - A clear, concise question
    - A factually correct, self-contained answer
    
    Content:
    {text}
    """
    
    try:
        # Generate content using structured outputs to guarantee JSON matching our schema
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FlashcardDeck,
                temperature=0.7,
            ),
        )
        
        # Pydantic will automatically parse and validate the JSON string into our model
        deck = FlashcardDeck.model_validate_json(response.text)
        return deck
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate flashcards using Gemini API: {e}")
