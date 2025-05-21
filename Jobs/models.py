from django.db import models
from UserAuth.models import industries

#choices for the job type:
job_types = (
    ("Rem", "Remote"),
    ("PT", "Part-Time"),
    ("FT", "Full-Time"),
)

class Job(models.Model):
    title = models.CharField(max_length=255, verbose_name="Job Title", help_text="Title of the job listing")
    description = models.TextField(blank=True, null=True)
    required_skills = models.ManyToManyField("Jobs.Skill", verbose_name=("required skills"))
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=3, choices=job_types)
    industry = models.CharField(max_length=50, choices=industries)
    salary_range = models.CharField(max_length=255, null=True, blank=True)
    posted_by = models.ForeignKey("UserAuth.RecruiterProfile", verbose_name=("posted by"), on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "Job"
        ordering = ["-posted_at", "is_active"]
    
    def __str__(self):
        return self.title
    

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = "Skill"
    
    
    def __str__(self):
        return self.name