from io import BytesIO
import docx2txt
import pdfminer.high_level

# cache decorator depends on Streamlit version
import streamlit as st
@st.cache_data

def extract_text(uploaded_file) -> str:
    """Extract text from PDF, DOCX, or plain text."""
    try:
        content_type = uploaded_file.type
        if 'pdf' in content_type:
            return pdfminer.high_level.extract_text(BytesIO(uploaded_file.read()))
        elif 'word' in content_type:
            return docx2txt.process(BytesIO(uploaded_file.read()))
        else:
            return uploaded_file.read().decode('utf-8')
    except Exception:
        return ''
