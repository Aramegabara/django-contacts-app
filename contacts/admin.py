from django.contrib import admin
from .models import Contact, ContactStatus


@admin.register(ContactStatus)
class ContactStatusAdmin(admin.ModelAdmin):
    """Admin interface for ContactStatus model."""
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model."""
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'status', 'date_added']
    list_filter = ['status', 'city', 'date_added']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'city']
    date_hierarchy = 'date_added'
    ordering = ['-date_added']
