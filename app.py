import PyPDF2
from gemini_utils import gemini_generate_flashcards

# --- Helper Functions ---
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def get_flashcards_from_llm(text, subject):
    return gemini_generate_flashcards(text, subject)

def parse_flashcards(llm_output):
    flashcards = []
    lines = llm_output.strip().split("\n")
    question, answer = None, None
    for line in lines:
        if line.strip().startswith("Q:"):
            question = line.strip()[2:].strip()
        elif line.strip().startswith("A:"):
            answer = line.strip()[2:].strip()
            if question and answer:
                flashcards.append({"Question": question, "Answer": answer})
                question, answer = None, None
    return flashcards



# --- Streamlit UI ---
def run_streamlit_app():
    import pandas as pd
    import streamlit as st
    import os
    from io import StringIO
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    st.set_page_config(page_title="LLM Flashcard Generator", layout="wide")
    st.title("📚 LLM Flashcard Generator")
    st.write("Generate question-answer flashcards from your study materials using AI!")

    with st.sidebar:
        st.header("Input Options")
        subject = st.selectbox("Subject (guides flashcard style):", ["General", "Biology", "History", "Computer Science", "Physics", "Chemistry", "Mathematics", "Other"])
        input_method = st.radio("Choose input method:", ["Upload .txt/.pdf", "Paste text"])

    if input_method == "Upload .txt/.pdf":
        uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf"])
        text_input = None
    else:
        uploaded_file = None
        text_input = st.text_area("Paste your educational content here:", height=250)

    if st.button("Generate Flashcards"):
        with st.spinner("Extracting text and generating flashcards..."):
            if uploaded_file:
                if uploaded_file.name.endswith(".pdf"):
                    text = extract_text_from_pdf(uploaded_file)
                else:
                    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    text = stringio.read()
            elif text_input:
                text = text_input
            else:
                st.error("Please provide input via file upload or paste text.")
                st.stop()
            if not text.strip():
                st.error("Input text is empty after extraction.")
                st.stop()
            try:
                llm_output = get_flashcards_from_llm(text, subject)
            except Exception as e:
                st.error(f"Error generating flashcards: {e}")
                st.stop()
            flashcards = parse_flashcards(llm_output)
            if len(flashcards) < 10:
                st.warning(f"Only {len(flashcards)} flashcards generated. Try with more content or a different subject.")
            st.session_state["flashcards"] = flashcards

    # --- Flashcard Review & Export ---
    if "flashcards" in st.session_state:
        st.subheader("Generated Flashcards")
        flashcards = st.session_state["flashcards"]
        df = pd.DataFrame(flashcards)
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state["flashcards"] = edited_df.to_dict("records")

        col1, col2 = st.columns(2)
        with col1:
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button("Export as CSV", csv, "flashcards.csv", "text/csv")
        with col2:
            json_str = edited_df.to_json(orient="records", indent=2)
            st.download_button("Export as JSON", json_str, "flashcards.json", "application/json")

if __name__ == "__main__":
    run_streamlit_app()
