import streamlit as st
from PyPDF2 import PdfReader
import easyocr
from dateutil import parser
import re

# Date normalization function
def normalize_dates(date_str):
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime('%m/%Y')  # Standardized format
    except:
        return date_str

# OCR text extraction function
def extract_text_from_image(pdf_path):
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English
    result = reader.readtext(pdf_path, detail=0)  # Extract text from the image
    return " ".join(result)

# Check if the PDF contains image-based content (for OCR support)
def is_image_based(pdf_path):
    return pdf_path.endswith('.png') or pdf_path.endswith('.jpg') or pdf_path.endswith('.jpeg')

# Function to parse the PDF (either text-based or image-based)
def parse_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    if is_image_based(pdf_path):  # Image-based PDF, use OCR
        text = extract_text_from_image(pdf_path)
    else:  # Text-based PDF, extract directly
        for page in reader.pages:
            text += page.extract_text()
    
    return text

# Extracting email, name, and other details from the resume text
def extract_information(text):
    # Extract name (assumed to be first line in resume)
    name = re.search(r'^[A-Z][a-z]+\s[A-Z][a-z]+', text)  # Simple regex for first and last name
    name = name.group(0) if name else None

    # Extract email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email.group(0) if email else None

    # Extract phone number (basic regex for common formats)
    phone = re.search(r'\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', text)
    phone = phone.group(0) if phone else None

    # Extract LinkedIn (basic regex for LinkedIn URL)
    linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+', text)
    linkedin = linkedin.group(0) if linkedin else None

    # Extract Skills
    skills = re.findall(r'(Python|SQL|R|Excel|Power BI|Tableau|Java|Machine Learning|Data Analysis)', text, re.IGNORECASE)

    return name, email, phone, linkedin, skills

# Main function to parse the resume and display structured data
def parse_resume(uploaded_file):
    if uploaded_file is not None:
        text = parse_pdf(uploaded_file)

        # Extracting data from text
        name, email, phone, linkedin, skills = extract_information(text)

        # Sample education and experience data (can be parsed similarly)
        education = [{"degree": "B.Tech", "institution": "XYZ University", "year": "2020"}]
        experience = [{"company": "ABC Corp", "title": "Data Analyst", "duration": "Jan 2020 - Dec 2022", "description": "Worked on AI models."}]
        
        # Apply Date Normalization
        for entry in education:
            entry['year'] = normalize_dates(entry['year'])
        
        for entry in experience:
            entry['duration'] = normalize_dates(entry['duration'])

        # Build confidence score (simple version, could be enhanced)
        confidence_scores = {
            "name_confidence": 1.0 if name else 0.0,
            "email_confidence": 1.0 if email else 0.0,
            "phone_confidence": 1.0 if phone else 0.0,
            "linkedin_confidence": 1.0 if linkedin else 0.0,
            "skills_confidence": 1.0 if skills else 0.0,
            "education_confidence": 1.0 if education else 0.0,
            "experience_confidence": 1.0 if experience else 0.0,
        }

        # Final parsed data output
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

        # Display structured output in Streamlit
        st.write(parsed_data)

# Streamlit UI Setup
st.title("Intelligent Resume Parser")
st.write("Upload a resume in PDF format to extract structured information.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file:
    parse_resume(uploaded_file)
