# Calendar System API

This project implements a calendar system that allows for scheduling meetings, detecting collisions, checking participant availability, and managing room accommodations.

## Prerequisites

Before starting, make sure you have the following installed on your system:

- Python 3.x
- PostgreSQL
- Virtualenv (for creating Python virtual environments)
- Django (installed via requirements)

## Setup Instructions

### 1. Install PostgreSQL
Install PostgreSQL and its additional components:
```bash
sudo apt install postgresql postgresql-contrib
```

### 2. Start PostgreSQL Service
Start the PostgreSQL service:
```bash
sudo systemctl start postgresql.service
```

### 3. Switch to PostgreSQL User
Switch to the postgres user to configure the database:
```bash
sudo -i -u postgres
```

### 4. Create Database
Once inside the postgres user shell, create a new database for the calendar system:
```bash
createdb calendar_system
```

### 5. Create a PostgreSQL User

### 6. Setup Python Virtual Environment
Exit from the postgres user shell and return to your regular user shell. Then, create and activate a Python virtual environment for the project:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 7. Install Requirements
Install the necessary Python dependencies by running:
```bash
pip install -r requirements.txt
```

### 8. Configure Database in Django
In the settings.py file of your Django project, update the database settings as follows:

```bash

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'calendar_system',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 9. Run Migrations
After configuring the database, make and apply migrations to set up the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 10. Start Django Development Server
To start the Django development server, run:
```bash
python manage.py runserver
```

### API Testing with Postman

You can use Postman to test the API by sending HTTP requests. Here's how:

    Open Postman.
    Create a new collection or request.
    Set the request method to POST, GET, PUT, or DELETE depending on the API functionality you are testing.
    Use the following URL format for requests: http://127.0.0.1:8000/api/your_endpoint/.
    Include the necessary headers (e.g., Content-Type: application/json) and body data (for POST or PUT requests).


### Additional Notes:

- Make sure you update the database credentials (username and password) in the `settings.py` file and in the readme file.
- This file assumes that your Django project and app are set up with the default directory structure. If you have different paths, adjust the instructions accordingly.
  
