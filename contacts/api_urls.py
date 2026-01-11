"""
API URL configuration for contacts application.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ContactViewSet, ContactStatusViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'statuses', ContactStatusViewSet, basename='status')

urlpatterns = [
    path('', include(router.urls)),
]
