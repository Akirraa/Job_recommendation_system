from django.contrib import admin
from UserAuth.models import User, JobSeekerProfile, RecruiterProfile
from Resume.models import Resume, ResumeData
from Applications.models import Application
from Jobs.models import Job, Skill
from Recommendations.models import Recommendation, UserVector, JobVector


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education', 'years_of_experience', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Automatically create Resume instance if resume file is uploaded
        if obj.resume and not Resume.objects.filter(user=obj.user, file=obj.resume).exists():
            Resume.objects.create(user=obj.user, file=obj.resume)


# Register other models normally
admin.site.register(User)
admin.site.register(RecruiterProfile)
admin.site.register(Resume)
admin.site.register(ResumeData)
admin.site.register(Application)
admin.site.register(Job)
admin.site.register(Skill)
admin.site.register(Recommendation)
admin.site.register(UserVector)
admin.site.register(JobVector)
