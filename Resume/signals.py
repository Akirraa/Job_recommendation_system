from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resume
from .tasks import parse_resumes

@receiver(post_save, sender=Resume)
def trigger_resume_processing(sender, instance, created, **kwargs):
    if created and instance.file:
        parse_resumes.delay(instance.id)
