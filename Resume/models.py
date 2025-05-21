from django.db import models
from django.core.validators import RegexValidator
import magic
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


def resume_format_validator(file):
    file_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if file_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise ValidationError("Unsupported file type")

class Resume(models.Model):
    user = models.ForeignKey("UserAuth.User", verbose_name=("user"), on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/", validators=[resume_format_validator], blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_text = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = "Resume"
        ordering = ["uploaded_at", "is_verified"]
        
    def __str__(self):
        return str(self.user)
    

class ResumeData(models.Model):
    resume_file = models.OneToOneField("Resume.Resume", verbose_name=("Resume File"), on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    skills = models.ManyToManyField("Jobs.Skill", blank=True)
    experience_summary = models.TextField(blank=True, null=True)
    education_summary = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = "ResumeData"
        
    def __str__(self):
        return self.candidate_name
