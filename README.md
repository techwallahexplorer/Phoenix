# Phoenix - LLM Flashcard Generator

Phoenix is a Streamlit app that generates editable flashcards from study material. It accepts pasted text or uploaded PDF, DOCX, and TXT files, then uses Gemini structured outputs with Pydantic validation to return a predictable flashcard format.

## What It Does

- Upload `.pdf`, `.docx`, or `.txt` files, or paste raw text.
- Choose a subject to guide the flashcard style.
- Generate question-answer flashcards using Gemini.
- Validate the LLM response with Pydantic models.
- Review and edit flashcards in the UI.
- Export flashcards as CSV or JSON.

## Tech Stack

- Streamlit
- Python
- Google GenAI SDK
- Pydantic
- PyPDF2
- python-docx
- Docker
- pytest

## Project Structure

```text
Phoenix/
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│   ├── app.py
│   ├── models/flashcard.py
│   ├── services/llm_service.py
│   └── utils/document_parser.py
└── tests/test_gemini_flashcards.py
```

## Local Setup

```bash
git clone https://github.com/techwallahexplorer/Phoenix.git
cd Phoenix
cp .env.example .env
pip install -r requirements.txt
streamlit run src/app.py
```

Set your Gemini key in `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Docker

```bash
docker build -t phoenix-flashcards .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_gemini_api_key_here phoenix-flashcards
```

## Testing

```bash
pytest tests/ -v
```

The test suite mocks Gemini calls so CI does not depend on live API keys.

## Notes

This project is a learning/product prototype. It demonstrates document parsing, LLM structured output handling, validation, and simple export workflows.
