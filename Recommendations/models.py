from django.db import models



class UserVector(models.Model):
    user = models.ForeignKey("UserAuth.User", verbose_name=("User"), on_delete=models.CASCADE, related_name="uservector")
    vector = models.JSONField()
    
    class Meta:
        db_table = "UserVector"
    
    def __str__(self):
        return str(self.user)
    
    
class JobVector(models.Model):
    job = models.ForeignKey("Jobs.Job", verbose_name=("Job"), on_delete=models.CASCADE, related_name="jobvector")
    vector = models.JSONField()
    
    class Meta:
        db_table = "JobVector"
    
    def __str__(self):
        return str(self.job)
    
class Recommendation(models.Model):
    user = models.ForeignKey("UserAuth.User", verbose_name=("User"), on_delete=models.CASCADE, related_name="recommendation")
    job = models.ForeignKey("Jobs.Job", verbose_name=("Job"), on_delete=models.CASCADE, related_name="recommendation")
    score = models.FloatField(help_text="Relevance score (higher = better match)")
    generated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "Recommendation"
        unique_together = ('user', 'job')
        verbose_name_plural = "Recommendations"
        ordering = ['-score', '-generated_at']

    
    def __str__(self):
        return f"{str(self.job)} -  {str(self.user)} - {self.generated_at}"


class RecommendationMetric(models.Model):
    date = models.DateField(auto_now_add=True)
    precision_at_5 = models.FloatField()
    sample_size = models.IntegerField()

    class Meta:
        db_table = "RecommendationMetrics"
        ordering = ['-date']

    def __str__(self):
        return f"Metrics on {self.date}: P@5={self.precision_at_5}, Sample={self.sample_size}"


class SemanticVector(models.Model):
    job = models.OneToOneField("Jobs.Job", on_delete=models.CASCADE)
    embedding = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.job)
