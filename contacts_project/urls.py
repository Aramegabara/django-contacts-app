"""
URL configuration for contacts_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contacts.urls')),
    path('api/', include('contacts.api_urls')),
]
