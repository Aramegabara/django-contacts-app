"""
URL configuration for contacts application.
"""

from django.urls import path
from .views import (
    ContactListView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
    import_contacts_csv,
    api_test_view,
)
from .weather_views import get_weather

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('contact/new/', ContactCreateView.as_view(), name='contact_create'),
    path('contact/<int:pk>/edit/', ContactUpdateView.as_view(), name='contact_edit'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),
    path('import-csv/', import_contacts_csv, name='import_csv'),
    path('api-test/', api_test_view, name='api_test'),
    path('weather/<str:city>/', get_weather, name='get_weather'),
]
