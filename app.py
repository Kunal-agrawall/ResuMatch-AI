import streamlit as st
from modules.parser import extract_text
from modules.matcher import calculate_similarity
from modules.feedback import suggest_improvements
import matplotlib.pyplot as plt

st.set_page_config(page_title="ResuMatch AI", layout="wide")
st.title("🚀 ResuMatch AI")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    threshold_good = st.slider("Good Match Threshold", 0.0, 1.0, 0.7, 0.05)
    threshold_ok = st.slider("Moderate Match Threshold", 0.0, threshold_good, 0.4, 0.05)

# File uploaders
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Resume (PDF, DOCX, TXT)", type=["pdf","docx","txt"])
with col2:
    job_file = st.file_uploader("Job Description (PDF, DOCX, TXT)", type=["pdf","docx","txt"])

if resume_file and job_file:
    st.info("Extracting...")
    resume_text = extract_text(resume_file)
    job_text = extract_text(job_file)

    if not resume_text or not job_text:
        st.error("Failed to parse files.")
    else:
        st.info("Matching...")
        score = calculate_similarity(resume_text, job_text)
        st.success(f"Match Score: {score*100:.2f}%")

        # Feedback
        if score >= threshold_good:
            st.balloons()
            st.write("🎉 Great match!")
        elif score >= threshold_ok:
            st.warning("👍 Moderate match.")
        else:
            st.error("⚠ Low match.")

        st.header("🔍 Suggestions to improve resume")
        suggestions = suggest_improvements(resume_text, job_text)
        for s in suggestions:
            st.markdown(f"- {s}")

        # Visualization
        labels=['Match','Gap']; values=[score,1-score]
        fig,ax=plt.subplots(); ax.pie(values,labels=labels,autopct='%1.1f%%'); ax.axis('equal')
        st.pyplot(fig)

else:
    st.info("Upload both files to analyze.")