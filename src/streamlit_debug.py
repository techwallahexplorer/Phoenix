import sys
import streamlit as st
st.write('Python executable:', sys.executable)
st.write('sys.path:', sys.path)
try:
    import PyPDF2
    st.write('PyPDF2 found!')
except ImportError:
    st.write('PyPDF2 NOT found!')
