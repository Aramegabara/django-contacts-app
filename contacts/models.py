"""
Models for the contacts application.

This module defines:
- ContactStatus: Available status choices for contacts
- Contact: Main contact model with personal information and status
"""

from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class ContactStatus(models.Model):
    """
    Model representing available status choices for contacts.
    
    Using a separate model allows for easy modification and extension
    of status choices from the database without code changes.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Contact Statuses"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Model representing a contact with personal information and status.
    
    Fields include validation for email and phone number uniqueness,
    as well as proper formatting validation.
    """
    
    # Name validator - only letters, spaces, hyphens, and apostrophes
    name_validator = RegexValidator(
        regex=r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+$",
        message="Name can only contain letters, spaces, hyphens, and apostrophes"
    )
    
    # Phone number validator - accepts various formats
    # Examples: +48123456789, 123-456-789, (12) 345-67-89
    phone_validator = RegexValidator(
        regex=r'^[\+\d][\d\s\-\(\)]{7,}$',
        message="Enter a valid phone number (min. 8 characters, digits, spaces, +, -, (, ) allowed)"
    )
    
    first_name = models.CharField(
        max_length=100,
        validators=[name_validator]
    )
    last_name = models.CharField(
        max_length=100,
        validators=[name_validator]
    )
    
    # Unique phone number with validation
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_validator],
        help_text="Phone number must be unique"
    )
    
    # Unique email with built-in validation
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Email address must be unique"
    )
    
    city = models.CharField(max_length=100)
    
    # ForeignKey to ContactStatus model as per requirements
    status = models.ForeignKey(
        ContactStatus,
        on_delete=models.PROTECT,  # Prevent deletion of status if contacts exist
        related_name='contacts'
    )
    
    date_added = models.DateTimeField(default=timezone.now)
    
    # Additional fields for better user experience
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']  # Most recent first by default
        indexes = [
            models.Index(fields=['last_name']),
            models.Index(fields=['date_added']),
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """Returns the full name of the contact."""
        return f"{self.first_name} {self.last_name}"
