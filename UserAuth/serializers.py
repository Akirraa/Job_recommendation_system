from rest_framework import serializers

from jobRecommandation import settings
from .models import User, JobSeekerProfile, RecruiterProfile
from Jobs.models import Skill

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes




# -----------------------
# User Serializer
# -----------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'full_name',
            'picture',
            'bio',
            'location',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# -----------------------
# Register Serializer
# -----------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'full_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            full_name=validated_data['full_name'],
            is_active=False # Set to False until email is verified
        )
        return user
    
    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        verification_url = f"http://localhost:8000/api/auth/verify-email/{uid}/{token}/"
        subject = "Verify your email for Smart Job"
        message = f"Hi {user.full_name},\n\nPlease verify your email by clicking the link below:\n{verification_url}\n\nIf you didn't register, please ignore this."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


# -----------------------
# Job Seeker Profile Serializer
# -----------------------
class JobSeekerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = serializers.SlugRelatedField(
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name',
        required=False
    )

    class Meta:
        model = JobSeekerProfile
        fields = [
            'id',
            'user',
            'education',
            'years_of_experience',
            'skills',
            'resume',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


# -----------------------
# Recruiter Profile Serializer
# -----------------------
class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = [
            'id',
            'user',
            'company_name',
            'company_website',
            'industry',
            'position',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
