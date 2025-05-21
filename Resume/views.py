from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Resume, ResumeData
from .serializers import ResumeSerializer, ResumeDataSerializer

from Jobs.pagination import JobPagination


class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeDataListView(generics.ListAPIView):
    serializer_class = ResumeDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination

    def get_queryset(self):
        return ResumeData.objects.filter(resume_file__user=self.request.user)


class ResumeDataRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ResumeDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResumeData.objects.filter(resume_file__user=self.request.user)
