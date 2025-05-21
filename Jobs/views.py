from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter

from .models import Job, Skill
from .serializers import JobSerializer, SkillSerializer
from .pagination import JobPagination


class SkillListCreate(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class SkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class JobListCreate(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    filterset_fields = ['job_type', 'industry', 'location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['posted_at', 'salary_range']
    
    #override the get defalt query set to filter the jobs based on the user
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)

        mine_param = self.request.query_params.get("mine")
        if mine_param and mine_param.lower() == "true":
            recruiter_profile = getattr(self.request.user, "recruiterprofile", None)
            if recruiter_profile:
                queryset = queryset.filter(posted_by=recruiter_profile)

        return queryset
    
    def perform_create(self, serializer):
        recruiter_profile = getattr(self.request.user, "recruiterprofile", None)
        if recruiter_profile is None:
            return Response({"detail": "Only recruiters can post jobs."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(posted_by=recruiter_profile)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        recruiter_profile = getattr(self.request.user, "recruiterprofile", None)
        if recruiter_profile != serializer.instance.posted_by:
            raise PermissionDenied("You do not have permission to edit this job.")
        serializer.save()

    def perform_destroy(self, instance):
        recruiter_profile = getattr(self.request.user, "recruiterprofile", None)
        if recruiter_profile != instance.posted_by:
            raise PermissionDenied("You do not have permission to delete this job.")
        instance.delete()
