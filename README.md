This project is an intelligent resume parsing tool built using Natural Language Processing (NLP) and Optical Character Recognition (OCR) techniques.
It extracts structured information from resumes in PDF format and presents it in a well-organized format,
including fields like name, email, phone, LinkedIn, skills, education, experience, certifications, and projects.

**Approach**
The approach to building the resume parser is broken down into the following steps:
1.Handling Different PDF Types:
-The script first checks whether the uploaded PDF is text-based or image-based.
-If it's text-based, we extract text directly using PyPDF2.
-If it's an image-based PDF (such as scanned documents), we use OCR (EasyOCR) to extract the text.
2.Data Extraction:
-Extract key fields from the parsed text, including full name, email, phone number, LinkedIn profile, skills, education, work experience, certifications, and projects.
-Use regular expressions to search for patterns that match emails, phone numbers, and LinkedIn URLs.
-A predefined list of common skills is used to intelligently extract technical skills from the resume text.
3.Date Normalization:
-Dates are normalized to a consistent format using the dateutil.parser library, which helps standardize various date formats (e.g., "Jan 2020 - Mar 2022").
4.Confidence Scores:
-Each extracted field includes a confidence score (ranging from 0 to 1), which reflects how likely the extraction is correct. A score of 1 indicates high confidence, and 0 indicates no extraction found for that field.
5.Structured Output:
-The final output is a JSON-like structure containing the parsed data and confidence scores, which is displayed on the Streamlit app for user review.

**Libraries/Tools Used**
-Streamlit: A framework to create interactive web applications. Used for the UI to upload PDFs and display results.
-PyPDF2: A library for PDF parsing. Used to extract text from text-based PDFs.
-EasyOCR: A library for Optical Character Recognition. Used to extract text from image-based PDFs.
-dateutil.parser: A date parsing library to handle various date formats and normalize them.
-re (Regular Expressions): Used for text pattern matching to identify key fields like email, phone, LinkedIn URLs, and skills.

**Assumptions**
-The resumes are in PDF format. The tool works with both text-based and image-based PDFs.
-The resume follows a typical structure with name, email, phone, skills, education, work experience, etc., but it may not be perfect for all formats.
-Skills are extracted from a predefined list, which may not cover every possible skill. Further expansion of the skill set list is possible.
-Some resumes may not contain all fields (e.g., certifications or projects). In such cases, the output will include null for missing field.

**Limitations**
-Accuracy of OCR: OCR accuracy may vary depending on the quality of the image-based PDF. Poor resolution or non-standard fonts may result in lower extraction accuracy.
-Skill Extraction: The skill extraction is based on a predefined list. Skills not present in the list might be missed unless expanded with a more sophisticated NLP model.
-Complex Formatting: Resumes with highly complex or non-standard formats may not be parsed perfectly.

