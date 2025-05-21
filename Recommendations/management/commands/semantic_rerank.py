from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer, util
import torch
from Recommendations.models import SemanticVector

from UserAuth.models import User
from Recommendations.models import Recommendation
from Recommendations.models import UserVector
from Resume.models import Resume

class Command(BaseCommand):
    help = "Re-rank top recommendations using Sentence-BERT embeddings"

    def handle(self, *args, **kwargs):
        model = SentenceTransformer('all-MiniLM-L6-v2')

        users = User.objects.filter(jobseekerprofile__isnull=False)

        for user in users:
            # Get top jobs from Layer 1 (TF-IDF) recommendations
            top_recs = Recommendation.objects.filter(user=user).order_by('-score')[:50]

            if not top_recs:
                continue

            job_texts = []
            job_ids = []
            job_objs = [] 

            for rec in top_recs:
                job = rec.job
                job_ids.append(job.id)
                job_texts.append(f"{job.title} {job.description}")
                job_objs.append(job)

    
            resume = Resume.objects.filter(user=user, parsed_text__isnull=False).first()

            if resume:
                user_input_text = resume.parsed_text
            elif UserVector.objects.filter(user=user).exists():
                user_input_text = " ".join(map(str, UserVector.objects.get(user=user).vector))
            else:
                continue  

            user_embedding = model.encode(user_input_text, convert_to_tensor=True)


            job_embeddings = []
            for job in job_objs:
                cached = SemanticVector.objects.filter(job=job).first()
                if cached:
                    emb = torch.tensor(cached.embedding)
                else:
                    emb = model.encode(f"{job.title} {job.description}", convert_to_tensor=True)
                    SemanticVector.objects.update_or_create(
                        job=job,
                        defaults={"embedding": emb.tolist()}
                    )
                job_embeddings.append(emb)

            job_embeddings = torch.stack(job_embeddings)


            # Compute cosine similarities
            similarities = util.cos_sim(user_embedding, job_embeddings)[0]

            # Re-rank by new semantic similarity
            scored_jobs = list(zip(job_ids, similarities.tolist()))
            scored_jobs.sort(key=lambda x: x[1], reverse=True)

            # Update Recommendation scores
            for job_id, semantic_score in scored_jobs:
                Recommendation.objects.filter(user=user, job__id=job_id).update(score=semantic_score)

        self.stdout.write(self.style.SUCCESS("Semantic re-ranking completed for all users."))
