from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from Jobs.models import Job
from Recommendations.models import JobVector

class Command(BaseCommand):
    help = "Generate and store TF-IDF vectors for active jobs"

    def handle(self, *args, **kwargs):
        jobs = Job.objects.filter(is_active=True)
        job_texts = [f"{job.title} {job.description}" for job in jobs]

        if not job_texts:
            self.stdout.write(self.style.WARNING("No active jobs found."))
            return

        vectorizer = TfidfVectorizer(stop_words="english", max_features=300)
        tfidf_matrix = vectorizer.fit_transform(job_texts)

        for i, job in enumerate(jobs):
            vector = tfidf_matrix[i].toarray().flatten().tolist()
            JobVector.objects.update_or_create(job=job, defaults={"vector": vector})

        self.stdout.write(self.style.SUCCESS("TF-IDF vectors generated for all active jobs."))
