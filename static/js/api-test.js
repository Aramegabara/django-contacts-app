// API Testing JavaScript

const API_BASE = '/api';

// Load statuses on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatuses();
});

// Load statuses for dropdowns
async function loadStatuses() {
    try {
        const response = await fetch(`${API_BASE}/statuses/`);
        const statuses = await response.json();
        
        const createSelect = document.getElementById('createStatus');
        const updateSelect = document.getElementById('updateStatus');
        
        statuses.forEach(status => {
            const option1 = new Option(status.name, status.id);
            const option2 = new Option(status.name, status.id);
            createSelect.add(option1);
            updateSelect.add(option2);
        });
    } catch (error) {
        console.error('Error loading statuses:', error);
    }
}

// GET All Contacts
document.getElementById('btnGetContacts').addEventListener('click', async () => {
    const resultEl = document.getElementById('contactsList');
    resultEl.textContent = 'Loading...';
    
    try {
        const response = await fetch(`${API_BASE}/contacts/`);
        const data = await response.json();
        resultEl.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultEl.textContent = `Error: ${error.message}`;
    }
});

// POST Create Contact
document.getElementById('createContactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultEl = document.getElementById('createResult');
    resultEl.style.display = 'block';
    resultEl.textContent = 'Creating...';
    
    const contactData = {
        first_name: document.getElementById('createFirstName').value,
        last_name: document.getElementById('createLastName').value,
        email: document.getElementById('createEmail').value,
        phone_number: document.getElementById('createPhone').value,
        city: document.getElementById('createCity').value,
        status: parseInt(document.getElementById('createStatus').value)
    };
    
    try {
        const response = await fetch(`${API_BASE}/contacts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(contactData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultEl.textContent = `✅ Success!\n\n${JSON.stringify(data, null, 2)}`;
            e.target.reset();
        } else {
            resultEl.textContent = `❌ Error!\n\n${JSON.stringify(data, null, 2)}`;
        }
    } catch (error) {
        resultEl.textContent = `❌ Error: ${error.message}`;
    }
});

// PUT Update Contact
document.getElementById('updateContactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultEl = document.getElementById('updateResult');
    resultEl.style.display = 'block';
    resultEl.textContent = 'Updating...';
    
    const contactId = document.getElementById('updateContactId').value;
    const contactData = {
        first_name: document.getElementById('updateFirstName').value,
        last_name: document.getElementById('updateLastName').value,
        email: document.getElementById('updateEmail').value,
        phone_number: document.getElementById('updatePhone').value,
        city: document.getElementById('updateCity').value,
        status: parseInt(document.getElementById('updateStatus').value)
    };
    
    try {
        const response = await fetch(`${API_BASE}/contacts/${contactId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(contactData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            resultEl.textContent = `✅ Success!\n\n${JSON.stringify(data, null, 2)}`;
        } else {
            resultEl.textContent = `❌ Error!\n\n${JSON.stringify(data, null, 2)}`;
        }
    } catch (error) {
        resultEl.textContent = `❌ Error: ${error.message}`;
    }
});

// DELETE Contact
document.getElementById('deleteContactForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultEl = document.getElementById('deleteResult');
    resultEl.style.display = 'block';
    resultEl.textContent = 'Deleting...';
    
    const contactId = document.getElementById('deleteContactId').value;
    
    if (!confirm(`Are you sure you want to delete contact #${contactId}?`)) {
        resultEl.textContent = 'Cancelled';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/contacts/${contactId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            resultEl.textContent = `✅ Contact #${contactId} deleted successfully!`;
            e.target.reset();
        } else {
            const data = await response.json();
            resultEl.textContent = `❌ Error!\n\n${JSON.stringify(data, null, 2)}`;
        }
    } catch (error) {
        resultEl.textContent = `❌ Error: ${error.message}`;
    }
});

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
