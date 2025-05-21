from celery import shared_task
from .utils import extract_resume_text, parse_resume_text

from .models import Resume, ResumeData
from Jobs.models import Skill
from phonenumber_field.phonenumber import PhoneNumber

@shared_task
def process_resume(resume_id):
    resume = Resume.objects.get(id=resume_id)
    file_path = resume.file.path

    text = extract_resume_text(file_path)
    resume.parsed_text = text
    resume.save()

    data = parse_resume_text(text)

    resume_data = ResumeData.objects.create(
        resume_file=resume,
        candidate_name=data["name"] or "Unknown",
        email=data["email"],
        phone_number=data["phone"] if data["phone"] else None,
        education_summary=data["education"],
        experience_summary=data["experience"],
        location=data["location"],
    )

    # Add skills if they exist in the DB
    for phrase in data["skills"]:
        skill = Skill.objects.filter(name__iexact=phrase).first()
        if skill:
            resume_data.skills.add(skill)

    resume_data.save()
