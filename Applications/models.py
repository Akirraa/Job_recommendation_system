from django.db import models

#Choices for applications choices
class ApplicationStatus(models.TextChoices):
    ACCEPTED = "Accepted", "Accepted"
    PENDING = "Pending", "Pending"
    REJECTED = "Rejected", "Rejected"
    WITHDRAWN = "Withdrawn", "Withdrawn"




#choices for interaction types 
class InteractionTypes(models.TextChoices):
    VIEWED = "Viewed", "Viewed"
    SKIPPED = "Skipped", "Skipped"
    SAVED = "Saved", "Saved"

class Application(models.Model):
    job = models.ForeignKey("Jobs.Job", verbose_name=("Job"), on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey("UserAuth.JobSeekerProfile", verbose_name=("Applicant"), on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey("Resume.Resume", verbose_name=("Resume"), on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Applications"
        ordering = ["-applied_at"]
        unique_together = ("job", "applicant")

    def __str__(self):
        return f'Application of {self.applicant.user.username} to {self.job.title}'
    
    
class Interaction(models.Model):
    user = models.ForeignKey("UserAuth.JobSeekerProfile", verbose_name=("User"), on_delete=models.CASCADE, related_name="interactions")
    job = models.ForeignKey("Jobs.Job", verbose_name=("Job"), on_delete=models.CASCADE, related_name="interactions")
    interaction_type = models.CharField(max_length=10, choices=InteractionTypes.choices)
    timestamp = models.DateTimeField(auto_now_add=True) #when the interaction occured
    
    class Meta:
        db_table = "Interactions"
        ordering = ["-timestamp"]
        unique_together = ("user", "job", "interaction_type")
        
        
    def __str__(self):
        return f'{str(self.user)} {self.interaction_type} {str(self.job)}'