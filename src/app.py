import os
import sys
import logging
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Set up relative imports from 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.llm_service import generate_flashcards_structured
from src.utils.document_parser import parse_uploaded_file

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Streamlit UI ---
def run_streamlit_app():
    # Load environment variables
    load_dotenv()
    
    st.set_page_config(page_title="LLM Flashcard Generator", layout="wide")
    st.title("📚 LLM Flashcard Generator")
    st.write("Generate high-quality structured flashcards from your study materials using AI!")

    with st.sidebar:
        st.header("Input Options")
        subject = st.selectbox("Subject (guides flashcard style):", ["General", "Biology", "History", "Computer Science", "Physics", "Chemistry", "Mathematics", "Other"])
        input_method = st.radio("Choose input method:", ["Upload .txt/.pdf/.docx", "Paste text"])

    text = ""
    if input_method == "Upload .txt/.pdf/.docx":
        uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf", "docx"])
        if uploaded_file:
            try:
                text = parse_uploaded_file(uploaded_file)
            except Exception as e:
                st.error(f"Error parsing file: {e}")
                logger.error(f"File parsing error: {e}")
    else:
        text = st.text_area("Paste your educational content here:", height=250)

    if st.button("Generate Flashcards", type="primary"):
        if not text or not text.strip():
            st.error("Please provide input via file upload or paste text.")
            st.stop()
            
        with st.spinner("Analyzing content and generating flashcards..."):
            try:
                # Use our new structured LLM service
                deck = generate_flashcards_structured(text, subject)
                
                # Convert Pydantic models to dicts for Streamlit
                flashcards = [{"Question": fc.question, "Answer": fc.answer} for fc in deck.flashcards]
                
                if len(flashcards) < 10:
                    st.warning(f"Only {len(flashcards)} flashcards generated. Try providing more content.")
                
                st.session_state["flashcards"] = flashcards
                st.success("Flashcards generated successfully!")
                logger.info(f"Generated {len(flashcards)} flashcards.")
                
            except Exception as e:
                st.error(f"Error generating flashcards: {e}")
                logger.error(f"Generation error: {e}")
                st.stop()

    # --- Flashcard Review & Export ---
    if "flashcards" in st.session_state:
        st.subheader("Generated Flashcards")
        flashcards = st.session_state["flashcards"]
        
        # Display as a dataframe for easy editing
        df = pd.DataFrame(flashcards)
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state["flashcards"] = edited_df.to_dict("records")

        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button("Export as CSV", csv, "flashcards.csv", "text/csv")
        with col2:
            json_str = edited_df.to_json(orient="records", indent=2)
            st.download_button("Export as JSON", json_str, "flashcards.json", "application/json")
            
        # UI visualization
        st.subheader("Preview Cards")
        for i, row in edited_df.iterrows():
            with st.expander(f"Q: {row['Question']}"):
                st.write(f"**Answer:** {row['Answer']}")

if __name__ == "__main__":
    run_streamlit_app()
