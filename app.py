import streamlit as st
import pdfplumber
import docx2txt
import pickle
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))



# Load model & vectorizer
with open("model.pkl", "rb") as f:
    model_data = pickle.load(f)
    model = model_data["model"]
    vectorizer = model_data["vectorizer"]

def preprocess(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [w for w in tokens if w not in stop_words]
    return " ".join(tokens)

def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return ""

def extract_skills(text, skills):
    text = text.lower()
    return [skill for skill in skills if skill in text]

# Skill database
skill_list = ['python', 'sql', 'machine learning', 'deep learning', 'nlp', 'pandas', 'excel', 'docker', 'tensorflow']

# UI
st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("📄 Resume Analyzer AI")

job_type = st.selectbox("Select Job Type", ["Data Scientist", "Web Developer", "AI Engineer", "Analyst"])
required_skills = st.multiselect("Select Required Skills", skill_list)
experience = st.selectbox("Experience Level", ["0-1 years", "1-3 years", "3-5 years", "5+ years"])
interests = st.multiselect("Select Your Interests", ["Data", "Web Dev", "AI/ML", "Finance", "Marketing"])
qualification = st.selectbox("Qualification", ["B.Tech", "M.Tech", "MCA", "PhD", "Others"])
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file and st.button("Analyze"):
    resume_text = extract_text(uploaded_file)
    if not resume_text.strip():
        st.error("Failed to extract text. Try another file.")
    else:
        combined_input = preprocess(resume_text + " " + " ".join(required_skills))
        vector_input = vectorizer.transform([combined_input])
        prediction = model.predict(vector_input)[0]

        resume_skills = extract_skills(resume_text, skill_list)
        matched = list(set(required_skills) & set(resume_skills))
        missing = list(set(required_skills) - set(resume_skills))
        match_percent = len(matched) / len(required_skills) * 100 if required_skills else 0

        st.subheader("📊 Analysis Report")
        st.markdown(f"**Job Type**: {job_type}")
        st.markdown(f"**Qualification**: {qualification}")
        st.markdown(f"**Experience Level**: {experience}")
        st.markdown(f"**Interests**: {', '.join(interests)}")
        st.markdown(f"**Matched Skills**: ✅ {', '.join(matched) if matched else 'None'}")
        st.markdown(f"**Missing Skills**: ❌ {', '.join(missing) if missing else 'None'}")
        st.markdown(f"**Match %**: `{match_percent:.2f}%`")

        if prediction == 1 and match_percent >= 75:
            st.success("✅ Great fit! You match most required skills.")
        elif prediction == 1:
            st.warning("⚠️ Partial fit. Improve missing skills.")
        else:
            st.error("❌ Not a good match. Consider learning more.")

