from django.core.management.base import BaseCommand
from Recommendations.models import RecommendationMetric
from Recommendations.utils.metrics import precision_at_k
from Applications.models import Interaction

class Command(BaseCommand):
    help = "Evaluate and store recommendation metrics"

    def handle(self, *args, **kwargs):
        k = 5
        precision = precision_at_k(k=k)
        sample_size = Interaction.objects.filter(interaction_type="Viewed").count()

        RecommendationMetric.objects.create(
            precision_at_5=precision,
            sample_size=sample_size
        )

        self.stdout.write(self.style.SUCCESS(
            f"Saved Precision@{k}: {precision} (Sample Size: {sample_size})"
        ))
