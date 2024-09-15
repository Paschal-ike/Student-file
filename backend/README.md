

# Backend Setup Documentation

## Overview

This backend is built using **Django** and **Django REST Framework**. It manages authentication, file uploads, and asynchronous processing of student voter data files.

### Prerequisites

- Python 3.8 or higher
- MySQL
- Redis (for task queue management with Dramatiq)
- Virtualenv (optional but recommended)

### Technologies Used

- **Django**: Core framework
- **Django REST Framework**: API creation
- **Dramatiq**: Asynchronous task processing
- **PostgreSQL**: Database
- **Pandas**: For data handling in uploaded files


## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Paschal-ike/Student-file
```

### 2. Create and Activate Virtual Environment

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
Create a .env file in the root directory
```

### 5. Run Database Migrations

Before starting the server, run migrations to set up your database

```bash
python manage.py migrate
```
### 6. Create Superuser

To create an admin account:
```bash
python manage.py createsuperuser

```
### 7. Run the Development Server

```bash
python manage.py runserver

```

### API Endpoints

### 1. Admin Login
Endpoint: /api/admin/login/
Method: POST
Description: Logs in an admin and returns a JWT token.

### 2. File Uploads
Endpoint: /api/admin/uploads/
Method: POST
Description: Allows the admin to upload CSV/Excel files. Files are processed asynchronously.

### 3. List Uploads
Endpoint: /api/admin/uploads/
Method: GET
Description: Retrieves a list of all uploaded files along with their statuses.
