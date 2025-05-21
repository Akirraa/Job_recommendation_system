from rest_framework import serializers
from .models import Job, Skill, job_types, industries

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']


class JobSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    required_skills_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        source='required_skills'
    )
    
    posted_by = serializers.StringRelatedField(read_only=True)
    posted_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'required_skills', 'required_skills_ids',
            'location', 'job_type', 'industry', 'salary_range', 'posted_by', 'posted_at', 'is_active'
        ]

    def validate_job_type(self, value):
        valid_types = [choice[0] for choice in job_types]
        if value not in valid_types:
            raise serializers.ValidationError("Invalid job type.")
        return value

    def validate_industry(self, value):
        valid_industries = [choice[0] for choice in industries]
        if value not in valid_industries:
            raise serializers.ValidationError("Invalid industry.")
        return value

    def create(self, validated_data):
        skills = validated_data.pop('required_skills', [])
        job = Job.objects.create(**validated_data)
        job.required_skills.set(skills)
        return job

    def update(self, instance, validated_data):
        skills = validated_data.pop('required_skills', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if skills is not None:
            instance.required_skills.set(skills)
        instance.save()
        return instance
