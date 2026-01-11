"""
REST API serializers for the contacts application.
"""

from rest_framework import serializers
from .models import Contact, ContactStatus


class ContactStatusSerializer(serializers.ModelSerializer):
    """Serializer for ContactStatus model."""
    
    class Meta:
        model = ContactStatus
        fields = ['id', 'name', 'description']


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model.
    
    Provides full contact information including status details.
    """
    status_name = serializers.CharField(source='status.name', read_only=True)
    
    class Meta:
        model = Contact
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'city',
            'status',
            'status_name',
            'date_added',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['date_added', 'created_at', 'updated_at']
    
    def validate_phone_number(self, value):
        """Ensure phone number is properly formatted."""
        if len(value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) < 8:
            raise serializers.ValidationError('Phone number must have at least 8 digits.')
        return value
    
    def validate_email(self, value):
        """Normalize email to lowercase."""
        return value.lower()


class ContactListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing contacts.
    
    Returns only essential fields as per API requirements:
    - id, first_name, last_name, city, status, date_added
    """
    status_name = serializers.CharField(source='status.name', read_only=True)
    
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'city', 'status_name', 'date_added']
