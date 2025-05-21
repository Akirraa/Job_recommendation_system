from django.urls import path
from .views import ApplicationListCreateView, ApplicationDetailView, InteractionListCreateView

urlpatterns = [
    path('applications/', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('interactions/', InteractionListCreateView.as_view(), name='interaction-list-create'),
]
