from celery import shared_task
from django.core.management import call_command

@shared_task
def generate_job_vectors():
    call_command("parse_resumes")