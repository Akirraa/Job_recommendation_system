import io
from pdfminer.high_level import extract_text
from transformers import pipeline
import re

# --------- 1. Extract Raw Text from PDF ---------
def extract_resume_text(resume_file):
    if resume_file.name.endswith(".pdf"):
        return extract_text(resume_file)
    return ""

# --------- 2. Clean and Normalize Text (optional step) ---------
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

# --------- 3. NLP-Based Resume Parser ---------
def parse_resume_text(text):
    cleaned = clean_text(text)

    # Load transformer model (zero-shot classification or NER)
    ner = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER")

    entities = ner(cleaned)
    results = {
        "name": None,
        "email": extract_email(text),
        "phone": extract_phone_number(text),
        "skills": [],
        "education": [],
        "experience": [],
        "location": None,
        "certifications": [],
        "projects": []
    }

    for entity in entities:
        label = entity["entity_group"]
        word = entity["word"]
        if label == "PER" and not results["name"]:
            results["name"] = word
        elif label == "ORG":
            results["experience"].append(word)
        elif label == "LOC":
            results["location"] = word
        elif label == "MISC":
            results["certifications"].append(word)

    # Use keyword-based fallbacks if needed
    return results

# --------- 4. Regex Helpers ---------
def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None

def extract_phone_number(text):
    match = re.search(r'(\+?\d{1,3})?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', text)
    return match.group(0) if match else None
