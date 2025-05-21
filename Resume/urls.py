from django.urls import path
from .views import ResumeListCreateView, ResumeRetrieveUpdateDestroyView, ResumeDataListView, ResumeDataRetrieveUpdateView

urlpatterns = [
    path('resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('resumes/<int:pk>/', ResumeRetrieveUpdateDestroyView.as_view(), name='resume-detail'),
    path('resume-data/', ResumeDataListView.as_view(), name='resume-data-list'),
    path('resume-data/<int:pk>/', ResumeDataRetrieveUpdateView.as_view(), name='resume-data-detail'),
]
