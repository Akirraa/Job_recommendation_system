from celery import shared_task
from django.core.management import call_command

@shared_task
def generate_job_vectors():
    call_command("generate_job_vectors")

@shared_task
def generate_user_vectors():
    call_command("generate_user_vectors")

@shared_task
def generate_recommendations():
    call_command("generate_recommendations")

@shared_task
def rerank_semantic_recommendations():
    call_command("semantic_rerank")
