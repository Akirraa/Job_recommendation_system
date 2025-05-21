from django.core.management.base import BaseCommand
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from UserAuth.models import User
from Jobs.models import Job
from Recommendations.models import UserVector, JobVector, Recommendation

class Command(BaseCommand):
    help = "Generate job recommendations based on TF-IDF similarity"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(jobseekerprofile__isnull=False)

        for user in users:
            try:
                user_vector_obj = UserVector.objects.get(user=user)
            except UserVector.DoesNotExist:
                continue

            user_vector = np.array(user_vector_obj.vector).reshape(1, -1)
            job_vectors = JobVector.objects.all()

            job_ids = []
            vectors = []
            for jv in job_vectors:
                if jv.vector:
                    job_ids.append(jv.job.id)
                    vectors.append(jv.vector)

            if not vectors:
                continue

            similarities = cosine_similarity(user_vector, np.array(vectors))[0]
            top_pairs = sorted(zip(job_ids, similarities), key=lambda x: x[1], reverse=True)[:10]

            for job_id, score in top_pairs:
                job = Job.objects.get(id=job_id)
                Recommendation.objects.update_or_create(user=user, job=job, defaults={"score": score})

        self.stdout.write(self.style.SUCCESS("TF-IDF job recommendations generated."))
