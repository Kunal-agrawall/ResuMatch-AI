import streamlit as st

@st.cache_data
def suggest_improvements(resume_text: str, job_text: str) -> list:
    """Generate simple keyword-based suggestions."""
    # identify missing keywords
    job_terms = set(job_text.lower().split())
    resume_terms = set(resume_text.lower().split())
    missing = list(job_terms - resume_terms)
    # pick top 5 frequent missing terms
    suggestions = [f"Include keyword '{w}'" for w in missing[:5]]
    return suggestions
