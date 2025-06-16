### 📄 Description
An AI-powered web app to analyze resumes against job requirements using NLP and machine learning. Users select job roles, upload resumes, and receive skill match analysis instantly.

---

# 🧠 Resume Analyzer AI

This is a Streamlit-based web application that helps users analyze their resumes by matching them with specific job types and required skills using Natural Language Processing (NLP) and Machine Learning (ML).

## 🚀 Features

- Upload resume in **PDF or DOCX** format
- Select:
  - Job Type
  - Required Skills
  - Experience Level
  - Interests
  - Qualification
- Extracts text from the resume
- Matches skills from resume with job requirements
- Predicts if the resume is a good fit using a trained ML model
- Displays:
  - Matched & missing skills
  - Match percentage
  - Fit recommendation

## 🧩 Tech Stack

- Python
- Streamlit
- scikit-learn
- NLTK
- SpaCy
- pdfplumber, docx2txt

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer-ai.git
   cd resume-analyzer-ai

Create virtual environment (optional):

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

Install dependencies:

pip install -r requirements.txt


Download NLTK stopwords:
python

import nltk
nltk.download('stopwords')

Run the app:

streamlit run app.py
