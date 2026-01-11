"""
REST API views for the contacts application.

Provides endpoints:
- GET /api/contacts/ - List all contacts
- POST /api/contacts/ - Create new contact
- PUT /api/contacts/{id}/ - Update contact
- DELETE /api/contacts/{id}/ - Delete contact
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Contact, ContactStatus
from .serializers import ContactSerializer, ContactListSerializer, ContactStatusSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact model providing full CRUD operations via REST API.
    
    Endpoints:
    - GET /api/contacts/ - List all contacts
    - POST /api/contacts/ - Create new contact
    - GET /api/contacts/{id}/ - Retrieve specific contact
    - PUT /api/contacts/{id}/ - Update contact
    - PATCH /api/contacts/{id}/ - Partial update contact
    - DELETE /api/contacts/{id}/ - Delete contact
    """
    queryset = Contact.objects.select_related('status').all()
    
    def get_serializer_class(self):
        """
        Use lightweight serializer for list view,
        full serializer for other actions.
        """
        if self.action == 'list':
            return ContactListSerializer
        return ContactSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new contact."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """Update an existing contact."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a contact."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for ContactStatus model (read-only).
    
    Provides list of available statuses for frontend.
    """
    queryset = ContactStatus.objects.all()
    serializer_class = ContactStatusSerializer
