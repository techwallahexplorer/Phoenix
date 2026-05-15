import PyPDF2
from docx import Document
import tempfile
from io import StringIO

def extract_text_from_pdf(file) -> str:
    """Extracts text from an uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file) -> str:
    """Extracts text from an uploaded DOCX file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file.getvalue())
        tmp_path = tmp.name
    doc = Document(tmp_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file) -> str:
    """Extracts text from an uploaded TXT file."""
    stringio = StringIO(file.getvalue().decode("utf-8"))
    return stringio.read()

def parse_uploaded_file(uploaded_file) -> str:
    """Detects file type and extracts text accordingly."""
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
