import streamlit as st
from pypdf import PdfReader
from main import analyze_resume


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, job_skills):

    job__text = " ".join(job_skills)
    documents = [resume_text, job__text]
    vectorizer = TfidfVectorizer()
    vectors= vectorizer.fit_transform(documents)
    similarity_matrix = cosine_similarity(vectors[0], vectors[1])
    return similarity_matrix[0][0] * 100

