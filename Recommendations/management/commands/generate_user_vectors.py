from django.core.management.base import BaseCommand
import numpy as np

from UserAuth.models import User
from Applications.models import Application, Interaction
from Recommendations.models import UserVector, JobVector

class Command(BaseCommand):
    help = "Generate and store user vectors"

    def handle(self, *args, **kwargs):
        users = User.objects.filter(jobseekerprofile__isnull=False)

        for user in users:
            interacted_job_ids = set()
            applied = Application.objects.filter(applicant__user=user).values_list("job_id", flat=True)
            interacted = Interaction.objects.filter(user__user=user).values_list("job_id", flat=True)
            interacted_job_ids.update(applied)
            interacted_job_ids.update(interacted)

            job_vectors = JobVector.objects.filter(job__id__in=interacted_job_ids)
            if not job_vectors.exists():
                continue

            vector_list = [np.array(jv.vector) for jv in job_vectors if jv.vector]
            if not vector_list:
                continue

            avg_vector = np.mean(vector_list, axis=0).tolist()

            UserVector.objects.update_or_create(user=user, defaults={"vector": avg_vector})

        self.stdout.write(self.style.SUCCESS("User vectors generated."))
