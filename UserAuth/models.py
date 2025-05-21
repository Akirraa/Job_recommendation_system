from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.core.validators import RegexValidator

from django.contrib.auth.models import BaseUserManager
#roles of users 
role_choices = (
    ("recruiter", "recruiter"),
    ("jobseeker", "job Seeker" ),
)

#education levels for job seekers
education_levels = (
    ("HS", "High School"),
    ("BA", "Bachelor's Degree"),
    ("MA", "Master's Degree"),
    ("PhD", "PhD"),
)

#industries for recruiter
industries = (
    ("tech", "Technology"),
    ("finance", "Finance"),
    ("healthcare", "Healthcare"),
    ("education", "Education"),
    ("construction", "Construction"),
    ("manufacturing", "Manufacturing"),
    ("retail", "Retail"),
    ("transport", "Transportation & Logistics"),
    ("legal", "Legal"),
    ("marketing", "Marketing & Advertising"),
    ("consulting", "Consulting"),
    ("hospitality", "Hospitality"),
    ("real_estate", "Real Estate"),
    ("energy", "Energy & Utilities"),
    ("government", "Government"),
    ("nonprofit", "Nonprofit"),
    ("media", "Media & Entertainment"),
    ("agriculture", "Agriculture"),
    ("telecom", "Telecommunications"),
    ("aerospace", "Aerospace & Defense"),
)

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


#custom users model (will be used as a 1 to 1 field in job seeker and recruiter models)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices= role_choices)
    full_name = models.CharField(max_length=100, validators=[RegexValidator(regex=r'^[a-zA-Z ]+$',message='The name must only contain letters and space', code="Invalid_name")])
    picture = models.ImageField(blank=True, null=True, default="user_pictures/default.png", upload_to="user_pictures/")
    bio = models.TextField(max_length=500, null=True, blank= True)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "User"
        ordering = ["full_name", "role"]
        
    def __str__(self):
        return f"{self.full_name}"
    
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    objects = CustomUserManager()




#job seeker users model
class JobSeekerProfile(models.Model):
    user = models.OneToOneField("UserAuth.User", verbose_name=("JobSeekerUser"), on_delete=models.CASCADE)
    education = models.CharField(max_length=3, choices=education_levels)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True, default=0)
    skills = models.ManyToManyField("Jobs.Skill", blank=True)
    resume = models.FileField(upload_to="resumes/", max_length=100, validators=[RegexValidator(regex=r'^.+\.(docx?|pdf)$', message='Upload must be in .doc, .docx or .pdf format', code='Bad_resume_Format')], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "JobSeekerProfile"
        
    def __str__(self):
        return f"{self.user.full_name}"
    


#recruiter users model
class RecruiterProfile(models.Model):
    user = models.OneToOneField("UserAuth.User", verbose_name=("RecruiterUser"), on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=50, choices=industries)
    position = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "RecruiterProfile"
        ordering = ["industry"]
        
    def __str__(self):
        return f"{self.user.full_name}"