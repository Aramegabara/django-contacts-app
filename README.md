# Contacts Manager - Django Web Application

Django application for managing contacts with weather integration and REST API. Created as a recruitment task for Supra Brokers S.A.

## 🌐 Live Demo

**Application URL:** https://ageraskov.pythonanywhere.com/

## Features

- **CRUD Operations**: Create, read, update, and delete contacts
- **Contact Fields**: First name, last name, phone, email, city, status, date added
- **Status Management**: ForeignKey relationship to ContactStatus model
- **Search & Sort**: Search by any field, sort by name or date
- **Validation**: Client-side and server-side validation (email, phone, names)
- **Weather Integration**: Real-time weather data from OpenStreetMap + Open-Meteo APIs
- **REST API**: Full CRUD operations via Django REST Framework
- **CSV Import**: Bulk import contacts from CSV file
- **Responsive UI**: Bootstrap 5 with mobile-friendly design

## Technology Stack

- Django 6.0.1 + Django REST Framework 3.15.2
- Bootstrap 5.3.0
- SQLite database
- JavaScript (Vanilla JS for AJAX and validation)

## Quick Start

### Option 1: Docker (Recommended) 🐳

1. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/contacts/

3. **Create superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Stop containers**
   ```bash
   docker-compose down
   ```

### Option 2: Manual Setup

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd django-contacts-app
   python -m venv env
   env\Scripts\activate  # Windows
   # source env/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

2. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py create_statuses
   python manage.py createsuperuser
   ```

3. **Run server**
   ```bash
   python manage.py runserver
   ```

4. **Access application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/contacts/

## Project Structure

```
django-contacts-app/
├── contacts/              # Main application
│   ├── models.py         # Contact and ContactStatus models
│   ├── views.py          # Web views (CRUD)
│   ├── forms.py          # Forms with validation
│   ├── api_views.py      # REST API views
│   ├── weather_views.py  # Weather API integration
│   └── admin.py          # Admin configuration
├── contacts_project/     # Project configuration
│   ├── settings.py       # Django settings
│   └── urls.py           # URL routing
├── templates/            # HTML templates
├── manage.py
└── requirements.txt
```

## Usage

### CSV Import Format
```csv
first_name,last_name,phone_number,email,city,status
John,Doe,+48123456789,john.doe@example.com,Warsaw,new
Jane,Smith,+48987654321,jane.smith@example.com,Krakow,in progress
```

### REST API Examples

**List contacts:**
```bash
GET http://127.0.0.1:8000/api/contacts/
```

**Create contact:**
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

**Update contact:**
```bash
PUT http://127.0.0.1:8000/api/contacts/1/
```

**Delete contact:**
```bash
DELETE http://127.0.0.1:8000/api/contacts/1/
```

## Key Features

### Validation
- Names: Only letters, spaces, hyphens, apostrophes (auto-capitalized)
- Email: Valid format, unique
- Phone: Min. 8 digits, unique
- Client-side (JavaScript) + Server-side (Django)

### Weather Integration
- Two-step: Geocoding (Nominatim) → Weather (Open-Meteo)
- Caching: 30 min (coords), 15 min (weather)
- AJAX loading, graceful error handling

### Performance
- Database indexes on search/sort fields
- `select_related()` for ForeignKey optimization
- Client-side caching for weather data

## Bonus Features (Additional Tasks)

✅ **Docker Support**: Full Docker and Docker Compose configuration for easy deployment
✅ **Caching**: Weather API caching (30 min for coordinates, 15 min for weather data)

---

**Created for Supra Brokers S.A. recruitment task**