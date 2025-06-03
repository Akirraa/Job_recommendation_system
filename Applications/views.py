from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


from .models import Application, Interaction
from .serializers import ApplicationSerializer, InteractionSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "jobseekerprofile"):
            return Application.objects.filter(applicant=user.jobseekerprofile)
        if hasattr(user, "recruiterprofile"):
            return Application.objects.filter(job__posted_by=user.recruiterprofile)
        return Application.objects.none()

    def perform_create(self, serializer):
        jobseeker = getattr(self.request.user, "jobseekerprofile", None)
        if not jobseeker:
            raise PermissionDenied("Only job seekers can apply for jobs.")
        serializer.save(applicant=jobseeker)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user = request.user
        jobseeker = getattr(user, "jobseekerprofile", None)
        recruiter = getattr(user, "recruiterprofile", None)

        # Job seeker can only update cover letter
        if jobseeker == instance.applicant:
            data = {'cover_letter': request.data.get('cover_letter', instance.cover_letter)}
        # Recruiter can only update application status
        elif recruiter == instance.job.posted_by:
            data = {'status': request.data.get('status', instance.status)}
        else:
            raise PermissionDenied("You do not have permission to update this application.")

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "jobseekerprofile", None) == instance.applicant:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to delete this application.")

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        jobseeker = getattr(user, "jobseekerprofile", None)
        recruiter = getattr(user, "recruiterprofile", None)

        if jobseeker and obj.applicant == jobseeker:
            return obj
        if recruiter and obj.job.posted_by == recruiter:
            return obj
        raise PermissionDenied("You do not have permission to access this application.")


class InteractionViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        jobseeker = getattr(self.request.user, "jobseekerprofile", None)
        if jobseeker:
            return Interaction.objects.filter(user=jobseeker)
        return Interaction.objects.none()

    def perform_create(self, serializer):
        jobseeker = getattr(self.request.user, "jobseekerprofile", None)
        if not jobseeker:
            raise PermissionDenied("Only job seekers can create interactions.")
        serializer.save(user=jobseeker)
