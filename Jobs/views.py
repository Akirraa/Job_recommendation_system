from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Job, Skill
from .serializers import JobSerializer, SkillSerializer
from .filters import JobFilter
from .pagination import JobPagination


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = JobFilter
    filterset_fields = ['job_type', 'industry', 'location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['posted_at', 'salary_range']

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)

        mine_param = self.request.query_params.get("mine")
        if mine_param and mine_param.lower() == "true":
            recruiter_profile = getattr(self.request.user, "recruiterprofile", None)
            if recruiter_profile:
                queryset = queryset.filter(posted_by=recruiter_profile)

        return queryset

    def create(self, request, *args, **kwargs):
        recruiter_profile = getattr(request.user, "recruiterprofile", None)
        if recruiter_profile is None:
            return Response({"detail": "Only recruiters can post jobs."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(posted_by=recruiter_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        recruiter_profile = getattr(request.user, "recruiterprofile", None)
        if recruiter_profile != instance.posted_by:
            raise PermissionDenied("You do not have permission to edit this job.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        recruiter_profile = getattr(request.user, "recruiterprofile", None)
        if recruiter_profile != instance.posted_by:
            raise PermissionDenied("You do not have permission to delete this job.")
        return super().destroy(request, *args, **kwargs)
