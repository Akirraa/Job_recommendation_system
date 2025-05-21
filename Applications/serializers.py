from rest_framework import serializers
from Jobs.models import Job
from Resume.models import Resume
from UserAuth.models import JobSeekerProfile
from .models import Application, Interaction


class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'resume', 'cover_letter',
            'status', 'applied_at'
        ]
        read_only_fields = ['status', 'applied_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'jobseekerprofile'):
            return data
        raise serializers.ValidationError("Only job seekers can apply for jobs.")

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['applicant'] = request.user.jobseekerprofile
        return super().create(validated_data)


class InteractionSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())

    class Meta:
        model = Interaction
        fields = ['id', 'job', 'interaction_type', 'timestamp']
        read_only_fields = ['timestamp']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request.user, 'jobseekerprofile'):
            return data
        raise serializers.ValidationError("Only job seekers can interact with jobs.")

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user.jobseekerprofile
        return super().create(validated_data)
