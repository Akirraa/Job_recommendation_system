from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resume
from .tasks import process_resume

@receiver(post_save, sender=Resume)
def trigger_resume_processing(sender, instance, created, **kwargs):
    if created and instance.file:
        process_resume.delay(instance.id)
