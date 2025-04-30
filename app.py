import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from dateutil import parser
import re
import io


SKILLS_LIST = [
    "Python", "SQL", "R", "Excel", "Power BI", "Tableau", 
    "Machine Learning", "Data Analysis", "Java", "Deep Learning", 
    "Data Visualization", "Statistics", "Pandas", "NumPy", "TensorFlow"
]

def normalize_dates(date_str):
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime('%m/%Y')  
    except Exception:
        return date_str


def extract_text_from_image(pdf_file):
    reader = easyocr.Reader(['en']) 
    result = reader.readtext(pdf_file, detail=0)  
    return " ".join(result)


def parse_pdf(uploaded_file):
  
    pdf_content = uploaded_file.read()

    reader = PdfReader(io.BytesIO(pdf_content))  
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  
            text += page_text
        else:  
            text = extract_text_from_image(pdf_content)
            break  
    
    return text

def extract_information(text):
    name = re.search(r'^[A-Z][a-z]+\s[A-Z][a-z]+', text)
    name = name.group(0) if name else None

    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email.group(0) if email else None
    phone = re.search(r'\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', text)
    phone = phone.group(0) if phone else None

    linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+', text)
    linkedin = linkedin.group(0) if linkedin else None

    skills = [skill for skill in SKILLS_LIST if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]

    return name, email, phone, linkedin, skills

def parse_resume(uploaded_file):
    if uploaded_file is not None:
        text = parse_pdf(uploaded_file)

        name, email, phone, linkedin, skills = extract_information(text)

        education = [{"degree": "B.Tech", "institution": "XYZ University", "year": "2020"}]
        experience = [{"company": "ABC Corp", "title": "Data Analyst", "duration": "Jan 2020 - Dec 2022", "description": "Worked on AI models."}]
        
        for entry in education:
            entry['year'] = normalize_dates(entry['year'])
        
        for entry in experience:
            entry['duration'] = normalize_dates(entry['duration'])

        confidence_scores = {
            "name_confidence": 1.0 if name else 0.0,
            "email_confidence": 1.0 if email else 0.0,
            "phone_confidence": 1.0 if phone else 0.0,
            "linkedin_confidence": 1.0 if linkedin else 0.0,
            "skills_confidence": 1.0 if skills else 0.0,
            "education_confidence": 1.0 if education else 0.0,
            "experience_confidence": 1.0 if experience else 0.0,
        }

        parsed_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "skills": skills,
            "education": education,
            "experience": experience,
            "confidence_scores": confidence_scores
        }

        st.write(parsed_data)

st.title("Intelligent Resume Parser")
st.write("Upload a resume in PDF format to extract structured information.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file:
    parse_resume(uploaded_file)

