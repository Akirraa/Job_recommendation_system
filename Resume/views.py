from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Resume, ResumeData
from .serializers import ResumeSerializer, ResumeDataSerializer
from Jobs.pagination import JobPagination


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeDataViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination

    def get_queryset(self):
        return ResumeData.objects.filter(resume_file__user=self.request.user)

    def get_serializer_class(self):
        return ResumeDataSerializer

    def perform_update(self, serializer):
        serializer.save()
