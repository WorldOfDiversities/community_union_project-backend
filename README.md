# Community Union Management System - Backend

Django REST API for the Community Union Management System.

## Quick Start

1. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements/development.txt
   ```

3. **Setup Environment**

   ```bash
   cp .env.example .env
   ```

4. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start Development Server**

   ```bash
   python manage.py runserver
   ```

   API available at: http://localhost:8000
   Admin at: http://localhost:8000/admin/

## Project Structure

- `config/` - Django project configuration (settings, URLs, WSGI/ASGI)
- `api/` - API routing and versioning
- `apps/` - Django applications
  - `accounts/` - User authentication & roles
  - `members/` - Member profiles
  - `activities/` - Union activities
  - `meetings/` - Meeting minutes & resolutions
  - `dues/` - Dues & payment tracking
  - `notifications/` - Announcements
  - `reports/` - Report generation

## Database

**Development:** Supabase PostgreSQL via `DATABASE_URL`
**Production:** Supabase PostgreSQL via `DATABASE_URL`

## Environment Variables

See `.env.example` for required variables.

Key variables:

- `DEBUG` - Enable debug mode (False in production)
- `SECRET_KEY` - Django secret (min 50 chars)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `DATABASE_URL` - Supabase PostgreSQL connection string
- `CORS_ALLOWED_ORIGINS` - Frontend origins

## Tech Stack

- **Framework:** Django 5.0
- **API:** Django REST Framework 3.15+
- **Auth:** SimpleJWT 5.3.2
- **Database:** Supabase PostgreSQL
- **Cache & Queue:** Redis + Celery
- **File Storage:** AWS S3 / Cloudinary (production)

## API Documentation

### Authentication

- `POST /api/v1/auth/login/` - Obtain JWT tokens
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `POST /api/v1/auth/logout/` - Logout & blacklist token
- `GET /api/v1/auth/me/` - Get current user profile

### Members

- `GET /api/v1/members/` - List members (paginated, filterable)
- `POST /api/v1/members/` - Register new member
- `GET /api/v1/members/{id}/` - Member detail
- `PUT/PATCH /api/v1/members/{id}/` - Update member
- `DELETE /api/v1/members/{id}/` - Archive member

### Activities

- `GET /api/v1/activities/` - List activities
- `POST /api/v1/activities/` - Create activity
- `POST /api/v1/activities/{id}/attendance/` - Mark attendance

### Meetings

- `GET /api/v1/meetings/` - List meetings
- `POST /api/v1/meetings/` - Create meeting
- `GET /api/v1/meetings/{id}/export/` - Export minutes as PDF

### Dues & Payments

- `GET /api/v1/dues/` - List dues records
- `PATCH /api/v1/dues/{id}/` - Record payment
- `GET /api/v1/dues/summary/` - Financial summary

## Available Commands

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
pytest

# Format code
black .
isort .

# Check code quality
flake8
pylint apps
```

## Development Roadmap

Phase 1 (Weeks 1-2): Authentication, base layout, member CRUD
Phase 2 (Weeks 3-4): Activities, meetings modules
Phase 3 (Weeks 5-6): Dues, reports, analytics
Phase 4 (Weeks 7-8): Settings, testing, deployment

## Deployment

### Railway / Render

1. Connect GitHub repository
2. Set environment variables
3. Add PostgreSQL and Redis add-ons
4. Configure start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. Run migrations: `python manage.py migrate`

## Documentation

See the root project documentation for full specification and design guidelines.
