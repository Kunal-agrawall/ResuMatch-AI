import streamlit as st
import docx2txt
import pdfminer.high_level
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Cached Vectorizer using new caching API ---
@st.cache_resource
def get_vectorizer():
    return HashingVectorizer(stop_words='english', n_features=8192)

# --- Cached Extraction ---
@st.cache_data
def extract_text(file):
    """
    Extract text from PDF, DOCX, or TXT, caching results for performance.
    """
    if file.type == "application/pdf":
        return pdfminer.high_level.extract_text(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    elif file.type.startswith("text"):
        return file.read().decode('utf-8')
    else:
        return ""

# --- Cached Similarity Calculation ---
@st.cache_data
def calculate_similarity(resume_text: str, job_text: str):
    """
    Compute cosine similarity using a fast HashingVectorizer (no fit overhead).
    """
    vectorizer = get_vectorizer()
    tfidf_matrix = vectorizer.transform([resume_text, job_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return score

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("👨‍💼 AI Resume Analyzer & Job Matcher")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Settings")
    threshold_good = st.slider("Good Match Threshold", 0.0, 1.0, 0.7, 0.05)
    threshold_ok = st.slider("Moderate Match Threshold", 0.0, threshold_good, 0.4, 0.05)

# File Uploaders
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
with col2:
    job_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

# Processing
if resume_file and job_file:
    st.info("Extracting text...")
    resume_text = extract_text(resume_file)
    job_text = extract_text(job_file)

    if not resume_text or not job_text:
        st.error("Could not extract text from one of the files.")
    else:
        st.info("Calculating similarity...")
        score = calculate_similarity(resume_text, job_text)
        st.success(f"Match Score: {score * 100:.2f}%")

        # Feedback
        if score >= threshold_good:
            st.balloons()
            st.write("🎉 **Great match! Your resume aligns well with the job.**")
        elif score >= threshold_ok:
            st.warning("👍 **Moderate match. Consider tailoring your resume more.**")
        else:
            st.error("⚠️ **Low match. Try adding relevant skills and experience.**")

        # Display snippets in expanders
        exp1 = st.expander("Extracted Resume Snippet")
        exp1.text(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))
        exp2 = st.expander("Extracted Job Description Snippet")
        exp2.text(job_text[:1000] + ("..." if len(job_text) > 1000 else ""))
else:
    st.write("Upload both Resume and Job Description to start analysis.")
