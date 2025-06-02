from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
import numpy as np

from UserAuth.models import User
from Resume.models import Resume, ResumeData
from Recommendations.models import UserVector

class Command(BaseCommand):
    help = "Generate and store user vectors based on resume data"

    def handle(self, *args, **kwargs):
        model = SentenceTransformer("all-MiniLM-L6-v2")

        users = User.objects.filter(jobseekerprofile__isnull=False)

        for user in users:
            print(f"Processing user: {user.email}")

            try:
                resume = Resume.objects.filter(user=user).order_by("-uploaded_at").first()
                if not resume:
                    print(f" - No resume found for user {user.email}")
                    continue

                resume_data = ResumeData.objects.get(resume_file=resume)

                skills_text = ", ".join([skill.name for skill in resume_data.skills.all()])
                combined_text = " ".join([
                    skills_text,
                    resume_data.experience_summary or "",
                    resume_data.education_summary or "",
                    resume_data.location or ""
                ]).strip()

                if not combined_text:
                    print(f" - No meaningful resume content for {user.email}")
                    continue

                embedding = model.encode(combined_text)
                UserVector.objects.update_or_create(user=user, defaults={"vector": embedding.tolist()})
                print(f" - UserVector saved for {user.email}")

            except ResumeData.DoesNotExist:
                print(f" - No ResumeData for the resume of user {user.email}")
                continue

        self.stdout.write(self.style.SUCCESS("User vectors generation based on resume data completed."))
