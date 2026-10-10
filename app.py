import os

import streamlit as st
from pypdf import PdfReader
from main import analyze_resume
from src.nlp_matcher import calculate_similarity
from database import create_database, save_analysis,get_all_analyses
create_database()
st.set_page_config(
    page_title="AI Career & Resume Analyzer",
    page_icon = "🤖",
    layout = "wide"
)
st.title("AI Career & Resume Analyzer")
st.write(
    "Analyze your resume , compare it with job requirements," 
    "identify skill gaps, and receive personalized recommendations."
)

uploaded_file = st.file_uploader(
    "upload your resume (PDF)",
    type=["pdf"]
)
full_text = ""
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    full_text = ""

    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    
    st.subheader("Resume Text")
    st.text_area("Extracted Text", value=full_text, height=300)

skills =[
    "Python",
    "SQL",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Analysis",
    "excel",
    "Power BI",
    "Git"
]

job_roles = {
    "data analyst": [
        "Python"
    ],
    "Python developer": [
        "Python",
        "Numpy",
        "SQL",
        "Git",
        "API",
    ],
    "AI/ML Intern":[
        "Python",
        "Machine Learning",
        "Artificial Intelligence",
        "Pandas",
        "NumPy",
        "Matplotlib"
    ]
}
st.subheader("Selected Job Roles")

selected_role = st.selectbox(
    "Choose a job role",
    list(job_roles.keys())
)
job_skills = job_roles[selected_role]

st.subheader("Job Description")
job_description = st.text_area(
    "paste the job description here",
    placeholder = "Example:Looking for a python developer with SQL and OOP skills.."
)
if job_description:
    st.subheader("Job Description Preview")
    st.write(job_description)

    if job_description:
        jd_similarity = calculate_similarity(
            full_text,
            [job_description]
        )
        st.subheader("Resume and job description ")
        st.metric(
            "JD Similarty",
            f"{jd_similarity:.2f}%"
        )
        if job_description:
            deteced_skills = []

            for skill in skills:
                if skill.lower() in job_description.lower():
                    deteced_skills.append(skill)

            st.subheader("skills dected in job description")
            if deteced_skills:
                for skill in deteced_skills:
                    st.success(skill)
            else:
                st.info("No skills detected in job description.")

st.subheader("Required skills")

for skill in job_skills:
    st.info(skill)
   
found_skills, missing_skills,matched_skills, match_percentage = analyze_resume(
    full_text,
    job_skills
)
st.write("DEBUG MATCHED:",
         matched_skills)
st.write("DEBUG MISSING:",
         missing_skills)
st.write("DEBUG FOUND:",
         found_skills)
st.write("DEBUG MATCH PERCENTAGE:",
         match_percentage)
similarity_score = calculate_similarity(full_text, job_skills)
st.subheader("NLP Match Score")
st.metric(
    "Resume and Job Similarity",
    f"{similarity_score:.2f}%"
)
if similarity_score > 70:
    st.success("Strong resume match for this job role!")
elif similarity_score > 40:
    st.warning("Good match , but some skills can be improved.")

else:
    st.error("Your resume needs more relevant skills for this job role.")

st.subheader("Resume Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Matched Skills")
    if matched_skills:
        for skill in matched_skills:
            st.success(skill)
    else:
        st.info("No matched skills found.")

with col2:
    st.subheader("Missing Skills")
    if missing_skills:
            st.write("you should focus on learnning these skills:")

            for skill in missing_skills:
               st.warning(skill)
    else:
        st.success("No missing skills")

st.subheader("Excellent! You have all the required skills for this job role." if not missing_skills else "You are missing some skills for this job role.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Match", f"{match_percentage:.2f}%")
with col2:
    st.metric("Matched", len(matched_skills))
with col3:
    st.metric("Missing", len(missing_skills))

st.progress(int(match_percentage))

st.subheader("Skill Analysis")

chart_data = {
    "Matched Skills": len(matched_skills),
    "Missing Skills": len(missing_skills)
}
st.bar_chart(chart_data)


st.subheader("Download Resume Analysis Report")
report = f"""
AI Career & Resume Analyzer
-----------------------------
Job Role: {selected_role}
Match Percentage: {match_percentage:.2f}%
Matched Skills:
{",".join(matched_skills) if matched_skills else "None"}
Missing Skills:
{",".join(missing_skills) if missing_skills else "None"}
"""
st.download_button(
    label="Download Report",
    data=report,
    file_name = "resume_analysis_report.txt",
    mime = "text/plain"
)
