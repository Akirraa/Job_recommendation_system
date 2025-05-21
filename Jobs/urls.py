from django.urls import path
from .views import SkillListCreate, SkillDetail, JobListCreate, JobDetail

urlpatterns = [
    # Skills endpoints
    path('skills/', SkillListCreate.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetail.as_view(), name='skill-detail'),

    # Jobs endpoints
    path('jobs/', JobListCreate.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'),
]
