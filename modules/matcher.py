import streamlit as st
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_resource
def get_vectorizer():
    return HashingVectorizer(stop_words='english', n_features=4096)

@st.cache_data
def calculate_similarity(text1: str, text2: str) -> float:
    """Fast cosine similarity via HashingVectorizer."""
    vect = get_vectorizer()
    mat = vect.transform([text1, text2])
    return float(cosine_similarity(mat[0:1], mat[1:2])[0][0])