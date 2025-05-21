import re
import spacy
from pdfminer.high_level import extract_text
from ...models import Resume, ResumeData
from Jobs.models import Skill

nlp = spacy.load("en_core_web_sm")  # or a transformer-based model

# Utility: Extract text from resume PDF
def extract_resume_text(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        print(f"[PDF Extract Error] {e}")
        return ""

# NLP Parsing Utility
def parse_resume_text(text):
    doc = nlp(text)
    
    # Extract email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = email_match.group(0) if email_match else None

    # Extract phone number (more robust pattern)
    phone_match = re.search(r"\+?\d[\d\-\s]{8,15}\d", text)
    phone = phone_match.group(0).strip() if phone_match else None

    # Extract name (first PERSON entity)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract education and experience summary (basic example)
    education = []
    experience = []
    for sent in doc.sents:
        if "education" in sent.text.lower():
            education.append(sent.text.strip())
        if "experience" in sent.text.lower() or "worked at" in sent.text.lower():
            experience.append(sent.text.strip())

    # Extract location
    location = None
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            location = ent.text
            break

    # Extract potential skill names using noun chunks (can be extended with BERT later)
    skill_phrases = set()
    for chunk in doc.noun_chunks:
        if 1 <= len(chunk.text) <= 40:
            skill_phrases.add(chunk.text.strip().lower())

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "education": "\n".join(education),
        "experience": "\n".join(experience),
        "location": location,
        "skills": list(skill_phrases),
    }
