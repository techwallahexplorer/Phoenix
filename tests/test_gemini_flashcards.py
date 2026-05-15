"""
Unit tests for Phoenix LLM Flashcard Generator.
Tests use mocking to avoid real API calls in CI.
"""
import sys
import os

# Ensure src/ is on the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO

# --- Tests for models/flashcard.py ---

from src.models.flashcard import Flashcard, FlashcardDeck

class TestFlashcardModels:
    def test_flashcard_creation(self):
        card = Flashcard(question="What is Python?", answer="A high-level programming language.")
        assert card.question == "What is Python?"
        assert card.answer == "A high-level programming language."

    def test_flashcard_deck_creation(self):
        cards = [
            Flashcard(question="Q1", answer="A1"),
            Flashcard(question="Q2", answer="A2"),
        ]
        deck = FlashcardDeck(flashcards=cards)
        assert len(deck.flashcards) == 2

    def test_flashcard_deck_from_json(self):
        json_str = '{"flashcards": [{"question": "What is AI?", "answer": "Artificial Intelligence."}]}'
        deck = FlashcardDeck.model_validate_json(json_str)
        assert len(deck.flashcards) == 1
        assert deck.flashcards[0].question == "What is AI?"

    def test_flashcard_requires_question_and_answer(self):
        with pytest.raises(Exception):
            Flashcard(question="Only a question")  # Missing 'answer'


# --- Tests for utils/document_parser.py ---

from src.utils.document_parser import extract_text_from_txt, parse_uploaded_file

class TestDocumentParser:
    def _make_mock_file(self, content: str, filename: str):
        """Helper to create a mock Streamlit uploaded file object."""
        mock_file = MagicMock()
        mock_file.name = filename
        mock_file.getvalue.return_value = content.encode("utf-8")
        return mock_file

    def test_extract_text_from_txt(self):
        mock_file = self._make_mock_file("Hello, world!", "notes.txt")
        result = extract_text_from_txt(mock_file)
        assert result == "Hello, world!"

    def test_parse_uploaded_file_txt(self):
        mock_file = self._make_mock_file("Sample content.", "sample.txt")
        result = parse_uploaded_file(mock_file)
        assert result == "Sample content."

    def test_parse_uploaded_file_unsupported_raises(self):
        mock_file = self._make_mock_file("data", "file.csv")
        with pytest.raises(ValueError, match="Unsupported file type"):
            parse_uploaded_file(mock_file)


# --- Tests for services/llm_service.py ---

from src.services.llm_service import generate_flashcards_structured

class TestLLMService:
    @patch("src.services.llm_service.genai")
    def test_generate_flashcards_returns_deck(self, mock_genai):
        """Test that the service correctly parses a valid structured response."""
        # Arrange: Mock the client and its response
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client

        valid_json = '{"flashcards": [{"question": "What is ML?", "answer": "Machine Learning."}]}'
        mock_response = MagicMock()
        mock_response.text = valid_json
        mock_client.models.generate_content.return_value = mock_response

        # Act
        deck = generate_flashcards_structured("Some text about ML", api_key="fake-key")

        # Assert
        assert isinstance(deck, FlashcardDeck)
        assert len(deck.flashcards) == 1
        assert deck.flashcards[0].question == "What is ML?"

    def test_generate_flashcards_raises_without_api_key(self):
        """Test that missing API key raises a clear ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            # Ensure GEMINI_API_KEY is not set
            os.environ.pop("GEMINI_API_KEY", None)
            with pytest.raises(ValueError, match="Gemini API key not set"):
                generate_flashcards_structured("Some text", api_key=None)
