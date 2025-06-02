from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ResumeDataViewSet

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'resume-data', ResumeDataViewSet, basename='resume-data')

urlpatterns = [
    path('', include(router.urls)),
]
