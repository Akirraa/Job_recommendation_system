import os
import re
import pdfplumber
import spacy
from django.core.management.base import BaseCommand
from Resume.models import Resume, ResumeData
from Jobs.models import Skill

nlp = spacy.load("en_core_web_sm")

EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_REGEX = re.compile(r"(\+?\d{1,3}[\s-])?(?:\(?\d{3}\)?[\s-])?\d{3}[\s-]?\d{4}")

class Command(BaseCommand):
    help = "Parse resumes with empty parsed_text and save parsed data"

    def extract_text_pdfplumber(self, file_path):
        try:
            with pdfplumber.open(file_path) as pdf:
                pages_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                return "\n".join(pages_text)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to extract text with pdfplumber: {e}"))
            return ""

    def extract_email(self, text):
        match = EMAIL_REGEX.search(text)
        return match.group(0) if match else ""

    def extract_phone(self, text):
        match = PHONE_REGEX.search(text)
        return match.group(0) if match else ""

    def extract_name(self, text):
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "Name":
                return ent.text
        return "Unknown"

    def extract_section(self, text, target_section_names):
        """
        Extract content of a section defined in target_section_names.
        Stops at the start of the next known section header.
        """
        all_section_names = [
            "Education", "Academic Background", "Educational Qualifications",
            "Experience", "Work Experience", "Professional Experience",
            "Skills", "Technical Skills", "Skills & Abilities", "Professional Skills",
            "Projects", "Certifications", "Achievements", "Contact",
            "Summary", "Location", "Address", "Personal Details", "Objective"
        ]

        # Regex to detect all section headers
        header_pattern = re.compile(rf"^\s*({'|'.join(all_section_names)})\s*[:\-]?\s*$", re.I | re.M)
        matches = list(header_pattern.finditer(text))
        if not matches:
            return ""

        section_text = ""
        for i, match in enumerate(matches):
            current_header = match.group(0).strip().lower()
            if any(target.lower() in current_header for target in target_section_names):
                start = match.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                section_text = text[start:end].strip()
                break

        return section_text

    def extract_skills_section(self, text):
        skills_section = self.extract_section(
            text, ["Skills", "Technical Skills", "Skills & Abilities", "Professional Skills"]
        )
        skills = re.split(r",|;|•|-|\n", skills_section)
        return [skill.strip() for skill in skills if skill.strip()]

    def handle(self, *args, **kwargs):


        resumes_to_parse = Resume.objects.filter(parsed_text__isnull=True)

        if not resumes_to_parse.exists():
            self.stdout.write("No resumes with empty parsed_text found.")
            return

        for resume in resumes_to_parse:
            if not resume.file or not os.path.isfile(resume.file.path):
                self.stdout.write(self.style.WARNING(f"Resume file not found for resume id={resume.id}"))
                continue

            self.stdout.write(f"Processing resume id={resume.id} for user {resume.user.email}")

            file_path = resume.file.path
            text = self.extract_text_pdfplumber(file_path)

            if not text.strip():
                self.stdout.write(self.style.WARNING(f"Could not extract text from file {resume.file.name}"))
                continue

            # Save raw extracted text
            resume.parsed_text = text
            resume.save()

            candidate_name = self.extract_name(text)
            email = self.extract_email(text)
            phone = self.extract_phone(text)

            education = self.extract_section(text, ["Education", "Academic Background", "Educational Qualifications"])
            experience = self.extract_section(text, ["Experience", "Work Experience", "Professional Experience"])
            location = self.extract_section(text, ["Location", "Address", "Contact Information"])
            skills_found = self.extract_skills_section(text)

            resume_data, created = ResumeData.objects.update_or_create(
                resume_file=resume,
                defaults={
                    "candidate_name": candidate_name,
                    "email": email,
                    "phone_number": phone,
                    "education_summary": education,
                    "experience_summary": experience,
                    "location": location,
                }
            )

            resume_data.skills.clear()
            for skill_name in skills_found:
                normalized = skill_name.lower()
                skill_obj, _ = Skill.objects.get_or_create(name=normalized)
                resume_data.skills.add(skill_obj)

            resume_data.save()
            self.stdout.write(self.style.SUCCESS(f"Parsed data saved for resume id={resume.id}"))

        self.stdout.write(self.style.SUCCESS("All applicable resumes parsed successfully."))
