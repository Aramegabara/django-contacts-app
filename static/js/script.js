// Client-side form validation for contact form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    
    if (!form) return; // Exit if form doesn't exist on page
    
    // Email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // Phone validation regex (min 8 chars, digits, spaces, +, -, (, ) allowed)
    const phoneRegex = /^[\+\d][\d\s\-\(\)]{7,}$/;
    
    form.addEventListener('submit', function(event) {
        let isValid = true;
        
        // Get form fields
        const firstName = document.getElementById('id_first_name');
        const lastName = document.getElementById('id_last_name');
        const email = document.getElementById('id_email');
        const phone = document.getElementById('id_phone_number');
        const city = document.getElementById('id_city');
        const status = document.getElementById('id_status');
        
        // Reset validation states
        [firstName, lastName, email, phone, city, status].forEach(field => {
            field.classList.remove('is-invalid', 'is-valid');
        });
        
        // Validate first name
        if (!firstName.value.trim()) {
            firstName.classList.add('is-invalid');
            isValid = false;
        } else if (!/^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+$/.test(firstName.value.trim())) {
            firstName.classList.add('is-invalid');
            isValid = false;
        } else {
            firstName.classList.add('is-valid');
        }
        
        // Validate last name
        if (!lastName.value.trim()) {
            lastName.classList.add('is-invalid');
            isValid = false;
        } else if (!/^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\-']+$/.test(lastName.value.trim())) {
            lastName.classList.add('is-invalid');
            isValid = false;
        } else {
            lastName.classList.add('is-valid');
        }
        
        // Validate email
        if (!email.value.trim() || !emailRegex.test(email.value.trim())) {
            email.classList.add('is-invalid');
            isValid = false;
        } else {
            email.classList.add('is-valid');
        }
        
        // Validate phone
        if (!phone.value.trim() || !phoneRegex.test(phone.value.trim())) {
            phone.classList.add('is-invalid');
            isValid = false;
        } else {
            // Additional check: count digits
            const digitCount = phone.value.replace(/\D/g, '').length;
            if (digitCount < 8) {
                phone.classList.add('is-invalid');
                isValid = false;
            } else {
                phone.classList.add('is-valid');
            }
        }
        
        // Validate city
        if (!city.value.trim()) {
            city.classList.add('is-invalid');
            isValid = false;
        } else {
            city.classList.add('is-valid');
        }
        
        // Validate status
        if (!status.value) {
            status.classList.add('is-invalid');
            isValid = false;
        } else {
            status.classList.add('is-valid');
        }
        
        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
            
            // Scroll to first error
            const firstError = form.querySelector('.is-invalid');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
        }
    });
    
    // Real-time validation on input
    const emailField = document.getElementById('id_email');
    const phoneField = document.getElementById('id_phone_number');
    
    if (emailField) {
        emailField.addEventListener('blur', function() {
            if (this.value.trim() && !emailRegex.test(this.value.trim())) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else if (this.value.trim()) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            }
        });
    }
    
    if (phoneField) {
        phoneField.addEventListener('blur', function() {
            if (this.value.trim()) {
                const digitCount = this.value.replace(/\D/g, '').length;
                if (!phoneRegex.test(this.value.trim()) || digitCount < 8) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                }
            }
        });
    }
});

// Weather API integration with caching for contact list
document.addEventListener('DOMContentLoaded', function() {
    const weatherContainers = document.querySelectorAll('.weather-container');
    const weatherCache = new Map();
    
    // Load weather for all contacts
    weatherContainers.forEach(container => {
        const city = container.dataset.city;
        loadWeather(container, city);
    });
    
    function loadWeather(container, city) {
        // Check cache first
        if (weatherCache.has(city)) {
            displayWeather(container, weatherCache.get(city));
            return;
        }
        
        // Fetch weather data
        fetch(`/weather/${encodeURIComponent(city)}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Weather data not available');
                }
                return response.json();
            })
            .then(data => {
                weatherCache.set(city, data);
                displayWeather(container, data);
            })
            .catch(error => {
                showWeatherError(container);
            });
    }
    
    function displayWeather(container, data) {
        const loadingEl = container.querySelector('.weather-loading');
        const infoEl = container.querySelector('.weather-info');
        const errorEl = container.querySelector('.weather-error');
        
        if (data && data.weather) {
            container.querySelector('.weather-temp').textContent = data.weather.temperature || 'N/A';
            container.querySelector('.weather-humidity').textContent = data.weather.humidity || 'N/A';
            container.querySelector('.weather-wind').textContent = data.weather.wind_speed || 'N/A';
            
            loadingEl.classList.add('d-none');
            errorEl.classList.add('d-none');
            infoEl.classList.remove('d-none');
        } else {
            showWeatherError(container);
        }
    }
    
    function showWeatherError(container) {
        const loadingEl = container.querySelector('.weather-loading');
        const infoEl = container.querySelector('.weather-info');
        const errorEl = container.querySelector('.weather-error');
        
        loadingEl.classList.add('d-none');
        infoEl.classList.add('d-none');
        errorEl.classList.remove('d-none');
    }
});

// CSV file validation for import form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('csvForm');
    const fileInput = document.getElementById('id_csv_file');
    
    if (!form || !fileInput) return; // Exit if form doesn't exist
    
    form.addEventListener('submit', function(event) {
        if (!fileInput.files || fileInput.files.length === 0) {
            event.preventDefault();
            alert('Please select a CSV file to upload.');
            return false;
        }
        
        const file = fileInput.files[0];
        
        // Check file extension
        if (!file.name.toLowerCase().endsWith('.csv')) {
            event.preventDefault();
            alert('Please upload a valid CSV file (.csv extension).');
            return false;
        }
        
        // Check file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            event.preventDefault();
            alert('File size should not exceed 5MB.');
            return false;
        }
    });
});

