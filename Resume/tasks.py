from celery import shared_task
from django.core.management import call_command

@shared_task
def parse_resumes():
    call_command("parse_resumes")