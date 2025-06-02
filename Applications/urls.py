from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, InteractionViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'interactions', InteractionViewSet, basename='interaction')

urlpatterns = [
    path('', include(router.urls)),
]
