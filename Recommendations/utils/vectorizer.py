from sklearn.feature_extraction.text import TfidfVectorizer
from Jobs.models import Job
from ..models import JobVector
import numpy as np

def build_job_corpus():
    jobs = Job.objects.all()
    corpus = []
    job_ids = []

    for job in jobs:
        text = f"{job.title} {job.description} {' '.join(skill.name for skill in job.required_skills.all())}"
        corpus.append(text)
        job_ids.append(job.id)
    
    return corpus, job_ids

def generate_job_vectors():
    corpus, job_ids = build_job_corpus()
    vectorizer = TfidfVectorizer(max_features=300)
    vectors = vectorizer.fit_transform(corpus).toarray()

    for i, job_id in enumerate(job_ids):
        JobVector.objects.update_or_create(
            job_id=job_id,
            defaults={'vector': vectors[i].tolist()}
        )
