"""
Forms for the contacts application.

Includes validation for email and phone number fields.
"""

from django import forms
from .models import Contact, ContactStatus


class ContactForm(forms.ModelForm):
    """
    Form for creating and editing contacts.
    
    Includes client-side validation attributes and custom error messages.
    """
    
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'city', 'status']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
                'required': True,
                'pattern': r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+",
                'title': 'Only letters, spaces, hyphens, and apostrophes allowed',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
                'required': True,
                'pattern': r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+",
                'title': 'Only letters, spaces, hyphens, and apostrophes allowed',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+48 123 456 789',
                'pattern': r'[\+\d][\d\s\-\(\)]{7,}',
                'title': 'Enter a valid phone number (min. 8 characters)',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
                'required': True,
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city name',
                'required': True,
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
        }
        error_messages = {
            'phone_number': {
                'unique': 'This phone number is already registered.',
            },
            'email': {
                'unique': 'This email address is already registered.',
            },
        }
    
    def clean_phone_number(self):
        """Additional validation for phone number."""
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove spaces for validation
            phone_clean = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if len(phone_clean) < 8:
                raise forms.ValidationError('Phone number must have at least 8 digits.')
        return phone
    
    def clean_first_name(self):
        """Additional validation for first name."""
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            import re
            if not re.match(r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+$", first_name):
                raise forms.ValidationError('First name can only contain letters, spaces, hyphens, and apostrophes.')
            # Capitalize first letter of each word
            first_name = first_name.title()
        return first_name
    
    def clean_last_name(self):
        """Additional validation for last name."""
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            import re
            if not re.match(r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+$", last_name):
                raise forms.ValidationError('Last name can only contain letters, spaces, hyphens, and apostrophes.')
            # Capitalize first letter of each word
            last_name = last_name.title()
        return last_name
    
    def clean_email(self):
        """Additional validation for email."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()  # Normalize to lowercase
        return email


class CSVImportForm(forms.Form):
    """
    Form for importing contacts from CSV file.
    
    Expected CSV format:
    first_name,last_name,phone_number,email,city,status
    """
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: first_name, last_name, phone_number, email, city, status',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv',
            'required': True,
        })
    )
    
    def clean_csv_file(self):
        """Validate that uploaded file is a CSV."""
        file = self.cleaned_data.get('csv_file')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('Please upload a valid CSV file.')
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size should not exceed 5MB.')
        return file
