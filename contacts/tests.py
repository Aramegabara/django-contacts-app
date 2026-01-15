"""
Unit tests for the contacts application.

Tests cover:
- Model validation and uniqueness constraints
- REST API CRUD operations
- Contact creation and data integrity
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Contact, ContactStatus


class ContactStatusModelTest(TestCase):
    """Test ContactStatus model."""
    
    def test_create_contact_status(self):
        """Test creating a contact status."""
        status = ContactStatus.objects.create(
            name="new",
            description="New contact"
        )
        self.assertEqual(str(status), "new")
        self.assertEqual(status.name, "new")


class ContactModelTest(TestCase):
    """Test Contact model validation and constraints."""
    
    def setUp(self):
        """Create test status for contacts."""
        self.status = ContactStatus.objects.create(name="new")
    
    def test_create_valid_contact(self):
        """Test creating a valid contact."""
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="john.doe@example.com",
            city="Warsaw",
            status=self.status
        )
        self.assertEqual(contact.get_full_name(), "John Doe")
        self.assertEqual(str(contact), "John Doe")
    
    def test_email_uniqueness(self):
        """Test that email must be unique."""
        Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="test@example.com",
            city="Warsaw",
            status=self.status
        )
        
        # Attempt to create another contact with same email
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                first_name="Jane",
                last_name="Smith",
                phone_number="+48987654321",
                email="test@example.com",  # Duplicate email
                city="Krakow",
                status=self.status
            )
    
    def test_phone_uniqueness(self):
        """Test that phone number must be unique."""
        Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="john@example.com",
            city="Warsaw",
            status=self.status
        )
        
        # Attempt to create another contact with same phone
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                first_name="Jane",
                last_name="Smith",
                phone_number="+48123456789",  # Duplicate phone
                email="jane@example.com",
                city="Krakow",
                status=self.status
            )
    
    def test_invalid_email_format(self):
        """Test validation for invalid email format."""
        contact = Contact(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="invalid-email",  # Invalid format
            city="Warsaw",
            status=self.status
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()


class ContactAPITest(APITestCase):
    """Test REST API endpoints for Contact."""
    
    def setUp(self):
        """Create test status and sample contact."""
        self.status = ContactStatus.objects.create(name="new")
        self.contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+48123456789",
            "email": "john.doe@example.com",
            "city": "Warsaw",
            "status": self.status.id
        }
        self.contact = Contact.objects.create(**{
            **self.contact_data,
            "status": self.status
        })
        self.list_url = reverse('contact-list')
        self.detail_url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
    
    def test_get_contact_list(self):
        """Test GET /api/contacts/ returns list of contacts."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'john.doe@example.com')
    
    def test_create_contact_via_api(self):
        """Test POST /api/contacts/ creates a new contact."""
        new_contact_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "+48987654321",
            "email": "jane.smith@example.com",
            "city": "Krakow",
            "status": self.status.id
        }
        response = self.client.post(self.list_url, new_contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'Jane')
    
    def test_update_contact_via_api(self):
        """Test PUT /api/contacts/{id}/ updates a contact."""
        updated_data = {
            "first_name": "John",
            "last_name": "Updated",
            "phone_number": "+48123456789",
            "email": "john.doe@example.com",
            "city": "Gdansk",
            "status": self.status.id
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.last_name, 'Updated')
        self.assertEqual(self.contact.city, 'Gdansk')
    
    def test_delete_contact_via_api(self):
        """Test DELETE /api/contacts/{id}/ deletes a contact."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)
    
    def test_create_contact_with_duplicate_email(self):
        """Test API rejects duplicate email."""
        duplicate_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "+48111222333",
            "email": "john.doe@example.com",  # Duplicate
            "city": "Poznan",
            "status": self.status.id
        }
        response = self.client.post(self.list_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
