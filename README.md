# Auth System

A minimal full-stack authentication boilerplate built with **Django REST Framework** and **Next.js**. Designed as a clean, reusable starting point for projects that need secure cookie-based JWT authentication.

---

## Overview

This project implements the core authentication flow — register, login, logout, token refresh, and fetching the current user — using **HttpOnly cookies** for secure token storage. It is intentionally small and focused, making it easy to extend into a larger application.

---

## Project Structure

```
Auth-System/
├── backend/
│   └── users/
│       ├── models/          # Custom user model (email-based, no username)
│       ├── managers/        # Custom user manager
│       ├── authentication/  # Cookie-based JWT authentication class
│       ├── serializers/     # Register, login, user serializers
│       ├── views/           # Auth views, token refresh, user info
│       └── urls.py          # All auth endpoints
│
└── frontend/
    ├── src/app/
    │   ├── page.js          # Home — shows user info, logout, token refresh
    │   ├── login/page.js    # Login form
    │   └── register/page.js # Registration form
    └── utils/auth.js        # All API calls (login, logout, register, refresh)
```

---

## Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Django | 6.0.5 | Web framework |
| Django REST Framework | 3.17.1 | REST API |
| SimpleJWT | 5.5.1 | JWT token generation & blacklisting |
| django-cors-headers | 4.9.0 | CORS handling |
| python-decouple | 3.8 | Environment variables |
| dj-database-url | 3.1.2 | Database URL config |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| Next.js | 15.1.0 | React framework |
| React | 19 | UI library |
| Axios | ^1 | HTTP client |
| Tailwind CSS | ^3 | Styling |

---

## How Authentication Works

1. **Register** — creates a new user with email + username + password
2. **Login** — validates credentials, generates a JWT access & refresh token pair, and sets them as **HttpOnly cookies** (`access_token`, `refresh_token`) — never exposed to JavaScript
3. **Authenticated requests** — the custom `CookieJWTAuthentication` class reads the `access_token` cookie on every request instead of expecting a Bearer header
4. **Token refresh** — the `/refresh/` endpoint reads the `refresh_token` cookie and issues a new `access_token` cookie silently
5. **Logout** — blacklists the refresh token server-side and deletes both cookies

### Cookie Settings
| Setting | Value |
|---|---|
| `httponly` | `True` — inaccessible to JavaScript |
| `secure` | `True` — HTTPS only |
| `samesite` | `None` — required for cross-site cookie sending |
| Access token lifetime | ~12 seconds (dev/testing value — increase for production) |
| Refresh token lifetime | 1 day |

> The access token lifetime is set to `0.2 minutes` (12 seconds) by default — this is intentionally short for testing the refresh flow. Set it to a sensible value (e.g. `timedelta(hours=1)`) before going to production.

---

## Getting Started

### Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with:
# SECRET_KEY=your-secret-key
# DEBUG=True
# ALLOWED_HOSTS=127.0.0.1,localhost
# DATABASE_URL=sqlite:///db.sqlite3

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend: `http://localhost:3000`  
Backend API: `http://localhost:8000/api/users/`

---

## API Endpoints

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| `POST` | `/api/users/register/` | Register a new user | No |
| `POST` | `/api/users/login/` | Login and set JWT cookies | No |
| `POST` | `/api/users/logout/` | Blacklist token and clear cookies | No |
| `POST` | `/api/users/refresh/` | Issue new access token from refresh cookie | No |
| `GET` | `/api/users/user-info/` | Get current user details | Yes |
| `PUT/PATCH` | `/api/users/user-info/` | Update current user details | Yes |

---

## User Model

The custom `CustomUser` model removes Django's default `username` field and uses **email as the unique identifier**:

```python
class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True)
    username = None   # removed
```

---

## Frontend Pages

| Page | Path | Description |
|---|---|---|
| Home | `/` | Shows user info if logged in; logout and refresh token buttons |
| Login | `/login` | Email + password login form |
| Register | `/register` | Username + email + password registration form |

All API calls are centralized in `utils/auth.js` using Axios with `withCredentials: true` to ensure cookies are sent cross-origin.

---

## Notes

- **Cookie auth instead of Bearer tokens** — the custom `CookieJWTAuthentication` class overrides SimpleJWT's default header-based auth to read from cookies instead
- **Token blacklisting is enabled** — `rest_framework_simplejwt.token_blacklist` is installed, so refresh tokens are invalidated on logout
- **CORS is fully open** (`CORS_ALLOW_ALL_ORIGINS = True`) and `CORS_ALLOW_CREDENTIALS = True` — tighten `CORS_ALLOWED_ORIGINS` before deploying to production
- This project is intentionally minimal — there are no roles, no additional models, and no pagination. It is designed to be a starting point you build on top of.
