<div align="center">

# 💬 CommentHub - Real-Time Comments Platform

### **Enterprise-grade commenting system with nested threads, rich media & instant notifications**

![Django](https://img.shields.io/badge/Django-5.2.10-092E20?style=for-the-badge&logo=django)
![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vue.js)
![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.4-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

[🚀 Live Demo](http://localhost) • [📖 API Docs](http://localhost:8000/api/schema/swagger-ui/) • [🔮 GraphQL Playground](http://localhost:8000/graphql/) • [🐛 Report Bug](https://github.com/jirniyjirniy/commenthub/issues)

</div>

---

## 🌟 Features at a Glance

<table>
<tr>
<td width="50%">

### 🎨 **Rich Content**
- **TipTap Editor** with formatting toolbar
- Markdown support & HTML preview
- Image uploads (JPG/PNG/GIF, auto-resize to 320x240)
- Text file attachments (TXT, max 100KB)
- XSS-safe HTML sanitization with bleach
- Cloudinary CDN integration

</td>
<td width="50%">

### ⚡ **Real-Time Experience**
- WebSocket notifications via Django Channels
- Instant reply alerts
- JWT-secured connections
- Live user presence
- Zero-refresh updates
- Redis-backed channel layers

</td>
</tr>
<tr>
<td width="50%">

### 🔒 **Enterprise Security**
- JWT authentication (access + refresh tokens)
- Google reCAPTCHA v2 validation
- CSRF protection
- Rate limiting
- SQL injection protection (Django ORM)
- XSS prevention (HTML sanitization)
- File type & size validation

</td>
<td width="50%">

### 🎯 **Smart Features**
- Infinite nested replies
- Username/email filtering
- Sort by date/popularity
- 25-item pagination
- Full-text search ready
- Email notifications (async via Celery)
- Redis caching for preview lists

</td>
</tr>
<tr>
<td width="50%">

### 🔌 **Modern APIs**
- **REST API** - Full CRUD operations
- **GraphQL API** - Flexible queries (Strawberry)
- **WebSocket API** - Real-time notifications
- **Swagger/OpenAPI** - Interactive documentation
- **GraphQL Playground** - Query exploration

</td>
<td width="50%">

### 🧪 **Testing & Quality**
- 26+ unit tests (100% model coverage)
- Isolated test environment (no Redis/RabbitMQ needed)
- Mock external services (reCAPTCHA, Cloudinary)
- Fast in-memory database tests
- Continuous integration ready

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

### Backend Architecture

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 5.2.10 | Core web framework |
| **Django REST Framework** | 3.16.2 | REST API endpoints |
| **Strawberry Django** | 0.73.5 | GraphQL API layer |
| **Django Channels** | 4.3.1+ | WebSocket support (ASGI) |
| **PostgreSQL** | 17 | Primary relational database |
| **Redis** | 7.4 | Cache backend & channel layers |
| **RabbitMQ** | 3.x | Message broker for Celery |
| **Celery** | 5.5.3+ | Distributed task queue |
| **Celery Beat** | 2.8.1+ | Periodic task scheduler |
| **Cloudinary** | Latest | CDN for media storage |
| **Simple JWT** | 5.5.1+ | JWT authentication |
| **Bleach** | 6.3.0+ | HTML sanitization |
| **Pillow** | 12.0.1+ | Image processing |

### Frontend Architecture

| Technology | Version | Purpose |
|------------|---------|---------|
| **Vue.js** | 3.5.24 | Progressive UI framework |
| **TypeScript** | 5.x | Type-safe development |
| **Pinia** | 3.0.4+ | State management |
| **Vue Router** | 4.6.3+ | Client-side routing |
| **TipTap** | 3.11.0+ | WYSIWYG rich text editor |
| **Tailwind CSS** | 3.x | Utility-first styling |
| **Vite** | Latest | Build tool & dev server |
| **Apollo Client** | 4.2.2+ | GraphQL client |

### Infrastructure

| Service | Purpose |
|---------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **Nginx** | Reverse proxy & static files |
| **Gunicorn/Uvicorn** | WSGI/ASGI server |

---

## 🚀 Quick Start (Docker)

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Git** for cloning repository

### One-Command Setup

```bash
# Clone repository
git clone git@github.com:jirniyjirniy/commenthub.git
cd commenthub

# Copy environment configuration
cp .env.example .env

# Edit .env with your credentials (required for production)
nano .env

# Build and start all services
docker-compose up --build

# In another terminal, run migrations
docker-compose exec backend python manage.py migrate

# Create superuser (optional)
docker-compose exec backend python manage.py createsuperuser
```

### Service Access Points

| Service | URL                                         | Credentials |
|---------|---------------------------------------------|-------------|
| 🎨 **Frontend** | http://localhost                            | - |
| 🔧 **Backend API** | http://localhost:8000/api/docs              | - |
| 📖 **ReDoc** | http://localhost:8000/api/schema/redoc/     | - |
| 🔮 **GraphQL Playground** | http://localhost:8000/graphql/              | - |
| 🗄️ **Django Admin** | http://localhost:8000/admin/                | superuser credentials |
| 🐰 **RabbitMQ Management** | http://localhost:15672                      | guest/guest |

---

## 💻 Local Development (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment (using uv - modern Python package manager)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
nano .env  # Edit with your credentials

# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Start Redis (required for caching & channels)
redis-server

# Start RabbitMQ (required for Celery)
# macOS: brew services start rabbitmq
# Linux: sudo systemctl start rabbitmq-server
# Or use Docker: docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Start Celery worker (in separate terminal)
uv run celery -A config worker -l info

# Start Celery beat scheduler (in separate terminal)
uv run celery -A config beat -l info

# Start development server
uv run uvicorn config.asgi:application --reload --host 0.0.0.0 --port 8000
# Or use: uv run python manage.py runserver
```

### Frontend Setup

```bash
cd vue_ui

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🧪 Running Tests

### Backend Tests (Recommended Method)

```bash
cd backend

# Run all tests with isolated test settings (no Redis/RabbitMQ needed)
uv run python manage.py test tests.tests --settings=config.test_settings

# Run with verbose output
uv run python manage.py test tests.tests --settings=config.test_settings -v 2

# Run specific test class
uv run python manage.py test tests.tests.CommentAPITest --settings=config.test_settings

# Run single test
uv run python manage.py test tests.tests.CommentAPITest.test_create_comment_authorized --settings=config.test_settings

# Keep test database between runs (faster)
uv run python manage.py test tests.tests --settings=config.test_settings --keepdb
```

### Test Coverage Report

```bash
# Install coverage
uv pip install coverage

# Run tests with coverage
uv run coverage run --source='app' manage.py test tests.tests --settings=config.test_settings

# Generate report
uv run coverage report

# Generate HTML report
uv run coverage html
# Open htmlcov/index.html in browser
```

### Frontend Tests

```bash
cd vue_ui

# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# Run tests in watch mode
npm run test:unit -- --watch
```

### Test Architecture

Our test suite includes:

- **26+ Unit Tests** covering:
  - ✅ User & Comment models
  - ✅ Serializers (HTML sanitization, validation)
  - ✅ REST API endpoints (CRUD operations)
  - ✅ WebSocket consumers
  - ✅ Email notifications
  - ✅ Cache invalidation
  - ✅ Authentication & permissions

- **Isolated Test Environment**:
  - In-memory SQLite database
  - Local cache (no Redis required)
  - Mocked external services (reCAPTCHA, Cloudinary)
  - Synchronous Celery tasks
  - Fast execution (~0.1s for full suite)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔐 DJANGO SECURITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECRET_KEY=your-super-secret-key-change-in-production-min-50-chars
DEBUG=True
PRODUCTION=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 💾 DATABASE (PostgreSQL)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DB_NAME=commenthub_db
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost  # or 'postgres' for Docker
DB_PORT=5432

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔴 REDIS (Cache & Channels)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REDIS_CACHE_URL=redis://127.0.0.1:6379/1
REDIS_HOST=127.0.0.1  # or 'redis' for Docker

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🐰 CELERY (RabbitMQ)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
# For Docker: amqp://guest:guest@rabbitmq:5672//

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ☁️ CLOUDINARY (CDN for uploads)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 RECAPTCHA (Google reCAPTCHA v2)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECAPTCHA_PUBLIC_KEY=your_public_key
RECAPTCHA_PRIVATE_KEY=your_private_key
VITE_RECAPTCHA_SITE_KEY=your_site_key

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📧 EMAIL (Gmail SMTP)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 FRONTEND (Vue.js)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VITE_API_BASE_URL=/api
VITE_API_HOST=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_GRAPHQL_URL=http://localhost:8000/graphql/

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 👤 DJANGO SUPERUSER (Auto-creation)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@commenthub.local
DJANGO_SUPERUSER_PASSWORD=admin123
```

---

## 📂 Project Structure

```
commenthub/
├── 📁 backend/                         # Django backend
│   ├── 📁 app/                         # Main application
│   │   ├── 📁 comments/               # Comments app
│   │   │   ├── migrations/
│   │   │   ├── templates/
│   │   │   │   └── emails/           # Email templates
│   │   │   ├── __init__.py
│   │   │   ├── admin.py              # Admin interface
│   │   │   ├── apps.py               # App config
│   │   │   ├── consumers.py          # WebSocket consumers
│   │   │   ├── exceptions.py         # Custom exceptions
│   │   │   ├── models.py             # Comment & User models
│   │   │   ├── routing.py            # WebSocket routing
│   │   │   ├── serializers.py        # DRF serializers
│   │   │   ├── signals.py            # Django signals (cache invalidation)
│   │   │   ├── tasks.py              # Celery tasks
│   │   │   ├── urls.py               # URL routing
│   │   │   └── views.py              # API views
│   │   ├── 📁 core/                   # Core utilities
│   │   │   └── utils.py              # Pagination & helpers
│   │   └── 📁 users/                  # User management
│   │       ├── models.py             # Custom User model
│   │       └── serializers.py
│   ├── 📁 config/                     # Django settings
│   │   ├── __init__.py
│   │   ├── asgi.py                   # ASGI config (WebSocket)
│   │   ├── celery.py                 # Celery configuration
│   │   ├── settings.py               # Main settings
│   │   ├── test_settings.py          # ✨ Test settings (isolated)
│   │   ├── urls.py                   # Root URL config
│   │   └── wsgi.py                   # WSGI config
│   ├── 📁 tests/                      # Test suite
│   │   ├── __init__.py
│   │   └── tests.py                  # 26+ unit tests
│   ├── 📁 templates/                  # Global templates
│   │   └── emails/                   # Email notification templates
│   ├── 📁 logs/                       # Application logs
│   ├── 📁 static/                     # Static files (collected)
│   ├── .env                          # Environment variables
│   ├── manage.py                     # Django CLI
│   ├── pyproject.toml                # Python dependencies (uv)
│   └── uv.lock
│
├── 📁 vue_ui/                         # Vue.js frontend
│   ├── 📁 public/                     # Static assets
│   ├── 📁 src/
│   │   ├── 📁 api/                    # API clients
│   │   │   ├── apollo.ts             # GraphQL client
│   │   │   └── comments.ts           # REST client
│   │   ├── 📁 components/            # Vue components
│   │   │   ├── CommentForm.vue
│   │   │   ├── CommentItem.vue
│   │   │   └── TipTapEditor.vue
│   │   ├── 📁 stores/                # Pinia stores
│   │   │   ├── auth.ts
│   │   │   └── comments.ts
│   │   ├── 📁 types/                 # TypeScript definitions
│   │   ├── 📁 views/                 # Page components
│   │   ├── 📁 router/                # Vue Router
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── index.css                 # Tailwind styles
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
│
├── 📁 docker/                         # Docker configs (optional)
├── .dockerignore
├── .gitignore
├── docker-compose.yml                # Multi-service orchestration
├── Dockerfile                        # Backend Docker image
├── LICENSE                           # MIT License
└── README.md                         # This file
```

---

## 🔌 API Documentation

### REST API Endpoints

#### Authentication

```http
POST   /api/register/                 # Register new user
POST   /api/login/                    # Login & get JWT tokens
POST   /api/token/refresh/            # Refresh access token
GET    /api/user/profile/             # Get current user profile
```

#### Comments

```http
GET    /api/comments/                 # List top-level comments (paginated)
POST   /api/comments/                 # Create new comment (auth required)
GET    /api/comments/{id}/            # Get specific comment with replies
PATCH  /api/comments/{id}/            # Update comment (owner only)
DELETE /api/comments/{id}/            # Delete comment (owner only)
GET    /api/comments/preview/         # Cached preview list
POST   /api/comments/preview-text/    # Preview HTML-sanitized text
GET    /api/comments/health/          # Health check
```

#### Query Parameters

```
?ordering=-created_at               # Sort by creation date (desc)
?ordering=user__username            # Sort by username
?search=searchterm                  # Search by username/email
?page=2                            # Pagination (25 items per page)
```

### WebSocket API

**Endpoint:** `ws://localhost:8000/ws/comments/{comment_id}/?token={jwt_token}`

**Connection:**
```javascript
const ws = new WebSocket(
  `ws://localhost:8000/ws/comments/1/?token=${accessToken}`
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'new_reply') {
    console.log('New reply:', data.data);
    // Update UI with new comment
  }
};
```

**Events:**
- `new_reply` - Sent when someone replies to the comment

---

## 📊 System Architecture

### High-Level Architecture

```
┌─────────────┐
│   Browser   │
│  (Vue.js)   │
└──────┬──────┘
       │ HTTP/WS/GraphQL
       ▼
┌─────────────────────────────────────┐
│         Nginx (Reverse Proxy)       │
└─────────────┬───────────────────────┘
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
┌──────────┐  ┌─────────────┐
│ Frontend │  │   Backend   │
│  Static  │  │   Django    │
│  Files   │  │  (ASGI/WSGI)│
└──────────┘  └──────┬──────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
        ▼            ▼            ▼              ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐
   │  Redis  │  │RabbitMQ │  │PostgreSQL│  │Cloudinary│
   │ (Cache) │  │(Broker) │  │  (DB)   │  │  (CDN)   │
   └─────────┘  └────┬────┘  └─────────┘  └──────────┘
                     │
                     ▼
                ┌─────────┐
                │ Celery  │
                │ Workers │
                └─────────┘
```

### Data Flow

1. **User Request** → Nginx → Django
2. **Authentication** → JWT validation
3. **CRUD Operations** → PostgreSQL
4. **File Upload** → Cloudinary CDN
5. **Cache Check** → Redis (preview lists)
6. **Real-time** → WebSocket via Django Channels
7. **Async Tasks** → Celery via RabbitMQ (email notifications)

---

## 🛡️ Security Features

### Implemented Security Measures

| Layer | Protection | Implementation |
|-------|-----------|----------------|
| **Authentication** | JWT tokens | djangorestframework-simplejwt |
| **Authorization** | Role-based access | Django permissions |
| **Password Security** | Argon2 hashing | Django Argon2 hasher |
| **CSRF** | Token validation | Django middleware |
| **XSS** | HTML sanitization | Bleach library |
| **SQL Injection** | ORM protection | Django ORM |
| **File Upload** | Type & size validation | Custom validators |
| **Rate Limiting** | Request throttling | Django-ratelimit (ready) |
| **HTTPS** | SSL/TLS support | Production config |
| **CORS** | Whitelist domains | django-cors-headers |

### Security Best Practices

```python
# Always use environment variables
SECRET_KEY = os.getenv("SECRET_KEY")  # Never commit to git

# Validate file uploads
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB for images
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif', '.txt']

# Sanitize HTML input
ALLOWED_TAGS = ['a', 'code', 'i', 'strong', 'p', 'br']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

# Use HTTPS in production
SECURE_SSL_REDIRECT = True  # when PRODUCTION=True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📈 Performance Optimizations

### Database

- **Indexes** on foreign keys (user_id, reply_id)
- **select_related()** for user joins
- **prefetch_related()** for nested replies
- **Database connection pooling**

### Caching Strategy

```python
# Cache preview list for 5 minutes
cache.set("comment_preview_list", data, timeout=300)

# Invalidate on new comment (via signals)
@receiver(post_save, sender=Comment)
def invalidate_cache(sender, instance, created, **kwargs):
    if created:
        cache.delete("comment_preview_list")
```

### Frontend

- **Lazy loading** for nested comments
- **Debouncing** for search input
- **Virtual scrolling** for large lists
- **Code splitting** with Vite
- **Image optimization** via Cloudinary

### WebSocket

- **Connection pooling** with Redis
- **Message batching** for multiple updates
- **Automatic reconnection**

---

## 🧩 Development Tools

### Code Quality

```bash
# Backend linting
uv run ruff check .           # Fast Python linter
uv run black .                # Code formatter
uv run mypy .                 # Type checker

# Frontend linting
cd vue_ui
npm run lint                  # ESLint
npm run format                # Prettier
```

### Database Migrations

```bash
# Create migration
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Show migration status
uv run python manage.py showmigrations
```

### Useful Commands

```bash
# Django shell with IPython
uv run python manage.py shell_plus

# Create superuser
uv run python manage.py createsuperuser

# Collect static files
uv run python manage.py collectstatic

# Check for issues
uv run python manage.py check

# Show URLs
uv run python manage.py show_urls
```

---

## 🚢 Production Deployment

### Environment Setup

```bash
# Set production environment variables
export DEBUG=False
export PRODUCTION=True
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Use production database
export DB_HOST=production-db-host.com

# Enable SSL
export SECURE_SSL_REDIRECT=True
```

### Docker Production Build

```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d

# Apply migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

### Recommended Production Stack

- **Server**: Ubuntu 22.04 LTS
- **Web Server**: Nginx
- **WSGI**: Gunicorn
- **ASGI**: Uvicorn
- **Database**: PostgreSQL 17 (managed service)
- **Cache**: Redis 7.4 (managed service)
- **Queue**: RabbitMQ (CloudAMQP)
- **CDN**: Cloudinary
- **Monitoring**: Sentry
- **Logging**: ELK Stack or Papertrail

---

## 🐛 Troubleshooting

### Common Issues

**Redis Connection Error**
```bash
# Start Redis
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:7.4-alpine
```

**RabbitMQ Connection Error**
```bash
# macOS
brew services start rabbitmq

# Linux
sudo systemctl start rabbitmq-server

# Docker
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

**Database Migration Issues**
```bash
# Reset migrations (development only!)
uv run python manage.py migrate --fake comments zero
uv run python manage.py showmigrations
uv run python manage.py migrate
```

**Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Tests Failing - Redis Required**
```bash
# Always use test settings
uv run python manage.py test tests.tests --settings=config.test_settings
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Write tests** for new features
4. **Run test suite**: `uv run python manage.py test tests.tests --settings=config.test_settings`
5. **Commit** changes: `git commit -m 'Add amazing feature'`
6. **Push** to branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### Code Standards

- Follow **PEP 8** for Python code
- Use **TypeScript** for frontend
- Write **docstrings** for functions
- Add **type hints** to Python code
- Maintain **test coverage** >80%
- Update **documentation** for new features

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

**Example:**
```
feat(comments): add GraphQL mutation for comment deletion

- Implemented deleteComment mutation
- Added permission checks
- Updated GraphQL schema documentation

Closes #123
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 jirniyjirniy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👨‍💻 Author & Maintainer

**Nikita Cerneckij (jirniyjirniy)**

- GitHub: [@jirniyjirniy](https://github.com/jirniyjirniy)
- Email: [nikitach.fw@gmail.com]()

---

## 🙏 Acknowledgments

Special thanks to:

- **Django** community for the amazing framework
- **Vue.js** team for the reactive UI library
- **Strawberry GraphQL** for elegant GraphQL support
- **Django Channels** for WebSocket capabilities
- **Cloudinary** for reliable media hosting
- **TipTap** team for the excellent editor
- All **open-source contributors**

---

## 📚 Additional Resources

### Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [Vue.js Guide](https://vuejs.org/guide/)
- [Celery Documentation](https://docs.celeryq.dev/)

### Related Projects

- [Django Channels](https://channels.readthedocs.io/)
- [TipTap Editor](https://tiptap.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

[![GitHub stars](https://img.shields.io/github/stars/jirniyjirniy/commenthub?style=social)](https://github.com/jirniyjirniy/commenthub/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/jirniyjirniy/commenthub?style=social)](https://github.com/jirniyjirniy/commenthub/network/members)

**[📖 Documentation](http://localhost:8000/api/schema/swagger-ui/)** • 
**[🐛 Report Bug](https://github.com/jirniyjirniy/commenthub/issues)** • 
**[✨ Request Feature](https://github.com/jirniyjirniy/commenthub/issues)**

---

Made with ❤️ by [jirniyjirniy](https://github.com/jirniyjirniy)

*Building the future of web comments, one feature at a time.*

</div>