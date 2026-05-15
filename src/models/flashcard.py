from pydantic import BaseModel, Field
from typing import List

class Flashcard(BaseModel):
    question: str = Field(..., description="A clear, concise question based on the educational content.")
    answer: str = Field(..., description="A factually correct, self-contained answer to the question.")

class FlashcardDeck(BaseModel):
    flashcards: List[Flashcard] = Field(..., description="A list of generated flashcards.")
