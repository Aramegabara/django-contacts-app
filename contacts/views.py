"""
Views for the contacts application.

Includes:
- Contact list with sorting
- Contact creation, editing, and deletion
- CSV import functionality
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import csv
import io

from .models import Contact, ContactStatus
from .forms import ContactForm, CSVImportForm


class ContactListView(ListView):
    """
    Display list of contacts with search and sorting functionality.
    """
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Contact.objects.select_related('status').all()
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(city__icontains=search_query)
            )
        
        # Sorting functionality
        sort_by = self.request.GET.get('sort', '-date_added')
        allowed_sorts = ['last_name', '-last_name', 'date_added', '-date_added', 'first_name', '-first_name']
        if sort_by in allowed_sorts:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-date_added')
        return context


class ContactCreateView(CreateView):
    """Create a new contact."""
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Contact created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ContactUpdateView(UpdateView):
    """Edit an existing contact."""
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Contact updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ContactDeleteView(DeleteView):
    """Delete a contact."""
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Contact deleted successfully!')
        return super().delete(request, *args, **kwargs)


@require_http_methods(["GET", "POST"])
def import_contacts_csv(request):
    """
    Import contacts from CSV file.
    
    Expected CSV format:
    first_name,last_name,phone_number,email,city,status
    """
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Read CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):  # Start from 2 (header is row 1)
                    try:
                        # Get or create status
                        status_name = row.get('status', '').strip()
                        if not status_name:
                            raise ValueError('Status is required')
                        
                        status, _ = ContactStatus.objects.get_or_create(
                            name=status_name,
                            defaults={'description': f'Status: {status_name}'}
                        )
                        
                        # Create contact
                        Contact.objects.create(
                            first_name=row.get('first_name', '').strip(),
                            last_name=row.get('last_name', '').strip(),
                            phone_number=row.get('phone_number', '').strip(),
                            email=row.get('email', '').strip().lower(),
                            city=row.get('city', '').strip(),
                            status=status
                        )
                        success_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {row_num}: {str(e)}")
                
                # Show results
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} contacts.')
                if error_count > 0:
                    error_msg = f'Failed to import {error_count} contacts. '
                    if len(errors) <= 5:
                        error_msg += 'Errors: ' + '; '.join(errors)
                    else:
                        error_msg += f'First 5 errors: ' + '; '.join(errors[:5])
                    messages.warning(request, error_msg)
                
                if success_count > 0:
                    return redirect('contact_list')
                    
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVImportForm()
    
    return render(request, 'contacts/import_csv.html', {'form': form})
