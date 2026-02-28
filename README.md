# UNICAL Fee Payment Portal API

This is the backend API for the University of Calabar (UNICAL) Fee Payment Portal. It is built with Django and Django REST Framework.

## Features

- Custom User Authentication (Admin, Staff, Student roles)
- JWT-based authentication using `djangorestframework-simplejwt`
- Role-specific dashboard endpoints
- OpenAPI documentation with `drf-spectacular`

## Project Structure

```
unical_fees_portal/
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── unical_fees_portal/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── README.md
```

## Setup and Installation

This project can be configured to run with a local SQLite database for development or a PostgreSQL database for production/staging.

### Local Development Setup (Recommended for Testing)

If you do not have access to the main PostgreSQL database, use this setup to test your application locally.

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd unical_fees_portal
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: For a local SQLite setup, you can remove `psycopg2-binary` from `requirements.txt` if you wish.*

4.  **Use the SQLite Database Configuration**
    In `unical_fees_portal/settings.py`, the `DATABASES` setting is already configured to use `db.sqlite3`.

5.  **Run Migrations to Create Your Local Database**
    This will create a `db.sqlite3` file in your project directory.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a Local Superuser**
    To test login and protected endpoints, create a local admin user.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your user.

    **Recommended Development Credentials:**
    - **Username:** `admin`
    - **Email:** `admin@unical.edu.ng`
    - **Password:** `admin123`

    To test the student role, you can either create another user or change the role of an existing user in the Django admin.

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    You can now test your API endpoints locally.

---

### Production/Staging Setup (PostgreSQL)

Use this setup when you are ready to connect to the legacy or production PostgreSQL database.

#### 1. Install Dependencies
Ensure `psycopg2-binary` is listed in your `requirements.txt` and installed.

#### 2. Configure the Connection to Your Database
In `unical_fees_portal/settings.py`, comment out the SQLite `DATABASES` configuration and uncomment the PostgreSQL one. Then, fill in the connection details for your database.

```python
# Use SQLite for local development
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# PostgreSQL configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',      # The name of your existing or new database
        'USER': 'your_db_user',      # The user for that database
        'PASSWORD': 'your_db_password',# The password for that user
        'HOST': 'localhost',         # Or the IP address/hostname where your DB is running
        'PORT': '5432',
    }
}
```

#### 3. Run Migrations (Use with Caution)
**Important:** Before running migrations, you need to assess the state of your legacy database.

*   **If you are starting with an empty database:** Run the migrations as normal.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
*   **If you are connecting to a legacy database where tables with the same names as your models already exist:** You need to "fake" the initial migration to sync Django's migration history with your existing schema.
    ```bash
    # This will mark the initial migrations as applied without actually running them
    python manage.py migrate --fake-initial
    ```
    After faking the initial migration, you can run `makemigrations` and `migrate` for any future model changes.

#### 4. Run the Server
```bash
python manage.py runserver
```



The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

- **Admin Login:** `POST /api/auth/login/`
- **Student Login:** `POST /api/auth/login/`
- **Refresh Token:** `POST /api/auth/token/refresh/`
- **Student Dashboard:** `GET /api/dashboard/student/` (Requires Student role)
- **Staff Dashboard:** `GET /api/dashboard/staff/` (Requires Staff role)
- **Admin Dashboard:** `GET /api/dashboard/admin/` (Requires Admin role)

## API Documentation

API documentation is available at the following endpoints:

- **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://127.0.0.1:8000/api/schema/redoc/`

---

## Frontend Integration Guide

This guide explains how the frontend application should interact with the backend API for authentication and accessing protected resources.

### 1. The Login Flow

The login process is the entry point for users. It authenticates them and provides the necessary information for the frontend to manage the session and user roles.

**Endpoint:** `POST /api/auth/login/`

#### Step 1: User Submits Credentials

The user enters their credentials (username, email, matric number, or staff ID) and password into the login form.

#### Step 2: Frontend Makes an API Call

The frontend sends an HTTP `POST` request to the login endpoint. The body of the request must be a JSON object with the following structure:

```json
{
    "username": "user_identifier",
    "password": "user_password"
}
```

- `username`: This field can contain the user's `username`, `email`, `matric_number` (for students), or `staff_id` (for admins). The backend will automatically figure out which it is.
- `password`: The user's password.

#### Step 3: Backend Sends a Response

If the credentials are valid, the backend will reply with a `200 OK` status and a JSON response containing the authentication tokens and user information. This response is specifically customized for this workflow:

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_role": "STUDENT",
    "user_id": 42,
    "full_name": "John Doe"
}
```

- `access_token`: A short-lived (5 minutes) JSON Web Token (JWT). This token must be sent with every request to a protected endpoint.
- `refresh_token`: A long-lived token used to get a new `access_token` when the old one expires.
- `user_role`: This is the most important field for the frontend. It will be `'ADMIN'`, `'STAFF'`, or `'STUDENT'`.
- `user_id`: The user's unique ID from the database.
- `full_name`: The user's full name, for display in the UI.

If credentials are invalid, the backend will respond with a `401 Unauthorized` error.

#### Step 4: Frontend Handles the Response

This is the key part for managing login roles:

1.  **Store Tokens:** The frontend must securely store the `access_token` and `refresh_token`. Common places are `localStorage`, `sessionStorage`, or a secure cookie (HttpOnly).
2.  **Redirect Based on Role:** The frontend must inspect the `user_role` field from the response and redirect the user accordingly:
    *   If `user_role` is `'STUDENT'`, navigate the user to the student dashboard page (e.g., `/dashboard/student`).
    *   If `user_role` is `'STAFF'`, navigate the user to the staff dashboard page (e.g., `/dashboard/staff`).
    *   If `user_role` is `'ADMIN'`, navigate the user to the admin dashboard page (e.g., `/dashboard/admin`).
3.  **Store User Info:** The frontend can store `user_id` and `full_name` in its state management solution (like Redux, Zustand, or React Context) to personalize the UI.

### 2. Making Authenticated Requests

To access protected endpoints like `/api/dashboard/student/` or `/api/dashboard/admin/`, the frontend must include the `access_token` in the request headers.

The header must be named `Authorization` and the value must be prefixed with `Bearer `.

**Example using JavaScript's `fetch` API:**

```javascript
const accessToken = localStorage.getItem('access_token'); // Or wherever you stored it

fetch('http://127.0.0.1:8000/api/dashboard/student/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    }
})
.then(response => response.json())
.then(data => {
    console.log(data); // "outstanding_fees", etc.
});
```

### 3. Handling Token Expiration

The `access_token` is designed to be short-lived. When it expires, API calls will fail with a `401 Unauthorized` error. When this happens, the frontend should:

1.  Use the `refresh_token` to get a new `access_token`.
2.  Make a `POST` request to the `/api/auth/token/refresh/` endpoint with the refresh token in the body:
    ```json
    {
        "refresh": "your_refresh_token"
    }
    ```
3.  The backend will respond with a new `access_token`.
4.  The frontend should store this new access token and retry the original failed request.

This token refresh logic is typically handled by an API client or an interceptor (e.g., using Axios interceptors).
# Unical-nexus-backend
