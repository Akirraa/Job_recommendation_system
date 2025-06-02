from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer

from Jobs.models import Job
from Recommendations.models import JobVector

class Command(BaseCommand):
    help = "Generate and store Sentence-BERT vectors for active jobs"

    def handle(self, *args, **kwargs):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        jobs = Job.objects.filter(is_active=True)

        if not jobs.exists():
            self.stdout.write(self.style.WARNING("No active jobs found."))
            return

        for job in jobs:
            job_text = f"{job.title} {job.description or ''}"
            embedding = model.encode(job_text)
            JobVector.objects.update_or_create(job=job, defaults={"vector": embedding.tolist()})

        self.stdout.write(self.style.SUCCESS("Sentence-BERT vectors generated for all active jobs."))
