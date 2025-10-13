# Train Station API Service

Django REST Framework API service for managing train station operations, including trains, routes, journeys, crew members, and ticket booking system.

## 📋 Features

- **JWT Authentication** for secure user access
- **Admin Panel** for managing train station operations
- **CRUD Operations** for stations, trains, routes, journeys, crews, and orders
- **Advanced Filtering** for trains (by train type) and routes (by source station)
- **Ticket Booking System** with seat validation and availability tracking
- **Image Upload** for train models
- **API Documentation** with Swagger and ReDoc
- **Permissions System** (Admin-only for modifications, authenticated users for read access)

## 🚀 Installing using GitHub

1. **Clone the repository**
```bash
git clone https://github.com/your-username/train-station-api.git
cd train-station-api
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root (see `.env.example`):
```env
# PostgreSQL settings
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data

# Django settings
SECRET_KEY=your_django_secret_key
DEBUG=True
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🐳 Run with Docker

1. **Build and run containers**
```bash
docker-compose up --build
```

The API will be available at `http://127.0.0.1:8000/`

## 🔑 Getting Access

### Demo Credentials (Testing)

You can use the following superuser account:
```
Email: admin@admin.com
Password: superuser
```

### Create Your Own User

1. **Register a new user:**
```
POST /api/user/register/
```
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

2. **Get access token:**
```
POST /api/user/token/
```
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

3. **Use the token in requests:**
```
Authorization: Bearer your-jwt-access-token-here
```

## 📖 API Documentation

- **Swagger UI:** `http://127.0.0.1:8000/api/doc/swagger/`
- **ReDoc:** `http://127.0.0.1:8000/api/doc/redoc/`