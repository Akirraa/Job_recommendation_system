from collections import defaultdict
from Recommendations.models import Recommendation
from Applications.models import Interaction

def precision_at_k(k=5):
    relevant_clicks = defaultdict(set)  # user_id -> set(job_ids)
    recommendations = defaultdict(list)  # user_id -> list(job_ids)

    # Get user interactions (views)
    interactions = Interaction.objects.filter(interaction_type="Viewed")
    for interaction in interactions:
        relevant_clicks[interaction.user.user.id].add(interaction.job.id)

    # Get top-K recommendations
    recs = Recommendation.objects.order_by('-score')
    for rec in recs:
        if len(recommendations[rec.user.id]) < k:
            recommendations[rec.user.id].append(rec.job.id)

    # Calculate precision@k
    total_precision = 0
    evaluated_users = 0

    for user_id in recommendations:
        recommended = recommendations[user_id]
        relevant = relevant_clicks.get(user_id, set())

        if not relevant:
            continue

        hits = sum(1 for job_id in recommended if job_id in relevant)
        precision = hits / k
        total_precision += precision
        evaluated_users += 1

    return round(total_precision / evaluated_users, 4) if evaluated_users else 0.0
