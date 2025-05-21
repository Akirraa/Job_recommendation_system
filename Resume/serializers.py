from rest_framework import serializers

from Jobs.models import Skill
from .models import Resume, ResumeData
from Jobs.serializers import SkillSerializer

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'uploaded_at', 'parsed_text', 'is_verified']
        read_only_fields = ['uploaded_at', 'parsed_text', 'is_verified']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ResumeDataSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skills_ids = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, write_only=True, source='skills')

    class Meta:
        model = ResumeData
        fields = [
            'id', 'resume_file', 'candidate_name', 'email', 'phone_number',
            'skills', 'skills_ids', 'experience_summary', 'education_summary', 'location'
        ]

    def create(self, validated_data):
        skills = validated_data.pop('skills', [])
        resume_data = ResumeData.objects.create(**validated_data)
        resume_data.skills.set(skills)
        return resume_data

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if skills is not None:
            instance.skills.set(skills)
        instance.save()
        return instance
