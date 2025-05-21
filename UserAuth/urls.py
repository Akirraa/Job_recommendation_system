from django.urls import path
from .views import RegisterView, LoginView, JobSeekerProfileView, RecruiterProfileView, PasswordResetRequestView, PasswordResetConfirmView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/jobseeker/', JobSeekerProfileView.as_view(), name='jobseeker-profile'),
    path('profile/recruiter/', RecruiterProfileView.as_view(), name='recruiter-profile'),
    
    
    # Password reset URLs
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    
    
    # Email verification URL
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),

]
