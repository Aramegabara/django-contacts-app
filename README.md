# Contacts Manager - Django Web Application

A full-featured web application for managing contacts, built with Django. This project was created as a recruitment task for Junior Fullstack Developer position at Supra Brokers S.A.

## Features

### Core Functionality
- ✅ **CRUD Operations**: Create, Read, Update, and Delete contacts
- ✅ **Contact Information**: First name, last name, phone number, email, city, status, date added
- ✅ **Status Management**: ForeignKey relationship to ContactStatus model for flexible status management
- ✅ **Sorting**: Sort contacts by last name or date added
- ✅ **Search**: Full-text search across all contact fields
- ✅ **Validation**: Client-side and server-side validation for email and phone number formats
- ✅ **Unique Constraints**: Automatic enforcement of unique phone numbers and emails

### Weather Integration
- ✅ **Real-time Weather Data**: Displays temperature, humidity, and wind speed for each contact's city
- ✅ **OpenStreetMap Nominatim API**: Geocoding city names to coordinates
- ✅ **Open-Meteo API**: Fetching current weather data
- ✅ **Caching**: Smart caching mechanism to minimize API requests

### REST API
- ✅ `GET /api/contacts/` - List all contacts
- ✅ `POST /api/contacts/` - Create new contact
- ✅ `GET /api/contacts/{id}/` - Retrieve specific contact
- ✅ `PUT /api/contacts/{id}/` - Update contact
- ✅ `PATCH /api/contacts/{id}/` - Partial update contact
- ✅ `DELETE /api/contacts/{id}/` - Delete contact
- ✅ `GET /api/statuses/` - List all available statuses

### CSV Import
- ✅ **Bulk Import**: Import multiple contacts from CSV file
- ✅ **Error Reporting**: Detailed error messages for failed imports
- ✅ **Sample CSV**: Downloadable sample file with proper format

### User Interface
- ✅ **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- ✅ **Modern UI**: Clean and intuitive design with Bootstrap Icons
- ✅ **Real-time Feedback**: AJAX-based weather loading without page refresh
- ✅ **Form Validation**: Interactive client-side validation with visual feedback

## Technology Stack

- **Backend**: Django 6.0.1
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **UI Framework**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons 1.11.0
- **API Framework**: Django REST Framework 3.15.2
- **Database**: SQLite (development)
- **HTTP Client**: Requests 2.32.3

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-contacts-app
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```bash
   python -m venv env
   env\Scripts\activate
   ```
   
   **Linux/macOS:**
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create initial status choices**
   ```bash
   python manage.py shell
   ```
   
   Then in the Python shell:
   ```python
   from contacts.models import ContactStatus
   
   statuses = [
       {'name': 'new', 'description': 'New contact'},
       {'name': 'in progress', 'description': 'Contact in progress'},
       {'name': 'lost', 'description': 'Lost contact'},
       {'name': 'outdated', 'description': 'Outdated contact'}
   ]
   
   for status_data in statuses:
       ContactStatus.objects.get_or_create(
           name=status_data['name'],
           defaults={'description': status_data['description']}
       )
   
   exit()
   ```

6. **Create superuser (for admin panel)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - API endpoints: http://127.0.0.1:8000/api/

## Project Structure

```
django-contacts-app/
├── contacts/                   # Main application
│   ├── migrations/            # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin interface configuration
│   ├── api_urls.py           # API URL routing
│   ├── api_views.py          # REST API views
│   ├── apps.py               # App configuration
│   ├── forms.py              # Form definitions with validation
│   ├── models.py             # Contact and ContactStatus models
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # Web URL routing
│   ├── views.py              # Web views (CRUD operations)
│   └── weather_views.py      # Weather API integration
├── contacts_project/          # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── templates/                 # HTML templates
│   ├── base.html             # Base template with navigation
│   └── contacts/
│       ├── contact_list.html           # Contact list with search/sort
│       ├── contact_form.html           # Create/edit form
│       ├── contact_confirm_delete.html # Delete confirmation
│       └── import_csv.html             # CSV import interface
├── static/                    # Static files (if needed)
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage Guide

### Managing Contacts

#### Add New Contact
1. Click "Add Contact" in navigation bar
2. Fill in all required fields:
   - First Name and Last Name
   - Phone Number (unique, min. 8 characters)
   - Email (unique, valid format)
   - City
   - Status
3. Click "Create Contact"

#### Edit Contact
1. Click "Edit" button on any contact card
2. Modify desired fields
3. Click "Update Contact"

#### Delete Contact
1. Click "Delete" button on any contact card
2. Confirm deletion on confirmation page

#### Search Contacts
1. Use search bar at top of contact list
2. Search by name, email, phone, or city
3. Click "Search" or press Enter

#### Sort Contacts
1. Click "Sort By" dropdown
2. Select sorting option:
   - Date Added (Newest/Oldest)
   - Last Name (A-Z/Z-A)

### Importing Contacts from CSV

1. Click "Import CSV" in navigation bar
2. Download sample CSV file (optional)
3. Prepare your CSV file with columns:
   ```
   first_name,last_name,phone_number,email,city,status
   ```
4. Upload the file
5. Review import results

**Example CSV:**
```csv
first_name,last_name,phone_number,email,city,status
John,Doe,+48123456789,john.doe@example.com,Warsaw,new
Jane,Smith,+48987654321,jane.smith@example.com,Krakow,in progress
```

### Using the REST API

#### List All Contacts
```bash
GET http://127.0.0.1:8000/api/contacts/
```

#### Create Contact
```bash
POST http://127.0.0.1:8000/api/contacts/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+48123456789",
  "email": "john.doe@example.com",
  "city": "Warsaw",
  "status": 1
}
```

#### Update Contact
```bash
PUT http://127.0.0.1:8000/api/contacts/1/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+48123456789",
  "email": "john.smith@example.com",
  "city": "Krakow",
  "status": 2
}
```

#### Delete Contact
```bash
DELETE http://127.0.0.1:8000/api/contacts/1/
```

#### Get Available Statuses
```bash
GET http://127.0.0.1:8000/api/statuses/
```

## Key Implementation Details

### Model Design
- **ContactStatus**: Separate model for status choices, allowing database-level modification
- **Contact**: Main model with validation and unique constraints
- Indexes on frequently queried fields (last_name, date_added, email, phone_number)

### Validation
- **Client-side**: JavaScript validation with Bootstrap styling
- **Server-side**: Django form and model validation
- **Unique constraints**: Enforced at database level

### Weather API Integration
- **Two-step process**: Geocoding → Weather data
- **Caching**: 30 minutes for coordinates, 15 minutes for weather data
- **Error handling**: Graceful degradation if API fails
- **Rate limiting**: Cache minimizes API requests

### Performance Optimizations
- `select_related()` for status ForeignKey queries
- Database indexes on search/sort fields
- AJAX loading for weather data (non-blocking)
- Client-side weather data caching

## Testing

You can test the application using:

1. **Web Interface**: Navigate through the UI and test all features
2. **Admin Panel**: Use Django admin to manage statuses and contacts
3. **API**: Use curl, Postman, or any HTTP client to test REST API
4. **CSV Import**: Test with the provided sample CSV format

## Future Enhancements

Potential improvements for production deployment:
- User authentication and authorization
- Contact categorization/tagging
- Export contacts to CSV
- Advanced filtering options
- Batch operations
- Email notifications
- Activity logging
- PostgreSQL for production database
- Docker containerization
- CI/CD pipeline

## Notes

- All code follows English naming conventions as required
- Comments are provided where necessary for complex logic
- The application uses Django's built-in security features
- CSRF protection is enabled for all forms
- Environment variables should be used for SECRET_KEY in production

## License

This project was created for educational and recruitment purposes.

## Contact

For questions or issues, please create an issue in the repository.

---

**Created as recruitment task for Supra Brokers S.A.**