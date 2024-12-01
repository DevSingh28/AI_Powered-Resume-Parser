import os
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai
import json

GEMINI_API_KEY = "AIzaSyAj3G3uc_4OZdcW6ovP-8RXIZosKfMKbXo"
genai.configure(api_key= GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(text[:200])
    return text

def extract_text_from_docx(file_path):
    """Extract text from a Word document."""
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    print(text[:500])
    return text


def parse_resume_with_gemini(text):
    """
    Extract structured information from a resume using Gemini Pro API.
    :param text: Resume text to process.
    :return: Parsed data as a dictionary or None if an error occurs.
    """
    prompt = f"""
    Extract the following information from the resume text:
    - Name
    - Education
    - Work Experience
    - Skills
    - Email Address
    - Phone Number
    - Location

    Resume Text:
    {text}

    Provide the information in JSON format with keys:
    {{
        "name": "Name here",
        "education": "Education here",
        "experience": "Experience details here",
        "skills": "Comma-separated skills",
        "email": "Email address",
        "contact_number": "Phone number",
        "location": "Location"
    }}
    """

    try:
        response = chat.send_message(prompt, stream=False)
        print(f"Raw response from Gemini Pro: {response.text}")
        cleaned_response = response.text.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        print(f"Cleaned response: {cleaned_response}")

        parsed_data = json.loads(cleaned_response)
        print(f"Parsed JSON: {parsed_data}")
        return parsed_data

    except json.JSONDecodeError as json_err:
        print(f"JSON parsing error: {json_err}")
        print(f"Raw response for debugging: {response.text}")
        return None
    except Exception as general_err:
        print(f"Error querying Gemini Pro: {general_err}")
        return None
