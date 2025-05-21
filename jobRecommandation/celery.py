import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobRecommandation.settings')

# Initialize Celery
app = Celery('jobRecommandation')

# Load settings from Django's settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()


# Configure periodic tasks using Celery beat
app.conf.beat_schedule = {
    'generate-job-vectors-every-day': {
        'task': 'Recommendations.tasks.generate_job_vectors',
        'schedule': crontab(hour=0, minute=0),  # daily at midnight
    },
    'generate-user-vectors-every-day': {
        'task': 'Recommendations.tasks.generate_user_vectors',
        'schedule': crontab(hour=1, minute=0),  # daily at 1AM
    },
    'generate-recommendations-every-day': {
        'task': 'Recommendations.tasks.generate_recommendations',
        'schedule': crontab(hour=2, minute=0),  # daily at 2AM
    },
    'rerank-semantic-recommendations-daily': {
        'task': 'Recommendations.tasks.rerank_semantic_recommendations',
        'schedule': crontab(hour=3, minute=0),  # daily at 3AM
    },
    'rerank-semantic-recommendations-every-3-minutes': {
    'task': 'Recommendations.tasks.rerank_semantic_recommendations',
    'schedule': crontab(minute='*/3'),
},

}
