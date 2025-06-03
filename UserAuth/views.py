#rest_framework imports
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
#password reset specific imports
from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_decode 
from rest_framework.generics import GenericAPIView 
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm 
from django.contrib.auth import get_user_model
#email verification specific imports
from django.utils.encoding import force_str
#internal imports
from .models import User, JobSeekerProfile, RecruiterProfile
from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    UserSerializer,
    JobSeekerProfileSerializer,
    RecruiterProfileSerializer,
    LoginSerializer
)
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.role == "jobseeker":
            JobSeekerProfile.objects.create(user=user)
        elif user.role == "recruiter":
            RecruiterProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


User = get_user_model()

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })



class JobSeekerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return JobSeekerProfile.objects.get(user=self.request.user)


class RecruiterProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return RecruiterProfile.objects.get(user=self.request.user)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


# Password Reset Views

class PasswordResetRequestView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        form = PasswordResetForm(data=serializer.validated_data)
        if form.is_valid():
            form.save(
                request=request,
                use_https=False,
                from_email='noreply@smartjobByRayaneKahlaoui.com',
                email_template_name='registration/password_reset_email.html'
            )
            return Response({"detail": "Password reset link sent."})
        return Response(form.errors, status=400)


class PasswordResetConfirmView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            form = SetPasswordForm(user=user, data={
                'new_password1': serializer.validated_data['new_password1'],
                'new_password2': serializer.validated_data['new_password2'],
            })

            if form.is_valid():
                form.save()
                return Response({"detail": "Password has been reset."})
            return Response(form.errors, status=400)

        return Response({"detail": "Invalid or expired token."}, status=400)   


#email verification view
class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'jobseeker-profile': reverse('jobseeker-profile', request=request, format=format),
        'recruiter-profile': reverse('recruiter-profile', request=request, format=format),
        'password-reset': reverse('password_reset', request=request, format=format),
        'verify-email': 'Use POST with uid/token to verify email (dynamic)',
    })
    
    
    
def placeholderView(request):
    return render(request, 'UserAuth/placeholder.html')