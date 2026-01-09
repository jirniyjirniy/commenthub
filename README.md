<div align="center">

# 💬 Real-Time Comments Platform

### **Enterprise-grade commenting system with nested threads, rich media & instant notifications**

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?style=for-the-badge&logo=vue.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

[🚀 Demo](http://localhost) • [📖 Docs](http://localhost:8000/api/schema/swagger-ui/) • [🐛 Report Bug](https://github.com/jirniyjirniy/commenthub/issues)

</div>

---

## 🌟 Features at a Glance

<table>
<tr>
<td width="50%">

### 🎨 **Rich Content**
- **TipTap Editor** with formatting toolbar
- Markdown support & HTML preview
- Image uploads (JPG/PNG/GIF)
- Text file attachments (TXT)
- XSS-safe HTML sanitization

</td>
<td width="50%">

### ⚡ **Real-Time Experience**
- WebSocket notifications
- Instant reply alerts
- JWT-secured connections
- Live user presence
- Zero-refresh updates

</td>
</tr>
<tr>
<td width="50%">

### 🔒 **Enterprise Security**
- JWT authentication
- Google reCAPTCHA v2
- CSRF protection
- Rate limiting
- Cloudinary CDN

</td>
<td width="50%">

### 🎯 **Smart Features**
- Infinite nested replies
- Username/email filtering
- Sort by date/popularity
- 25-item pagination
- Full-text search ready

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

<details open>
<summary><b>Backend Technologies</b></summary>

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 5.2 | Core framework |
| **DRF** | Latest | REST API |
| **Channels** | Latest | WebSocket |
| **PostgreSQL** | 14+ | Primary database |
| **Redis** | 7+ | Cache & broker |
| **Celery** | Latest | Task queue |
| **Cloudinary** | Latest | Media storage |

</details>

<details>
<summary><b>Frontend Technologies</b></summary>

| Technology | Version | Purpose |
|------------|---------|---------|
| **Vue.js** | 3.x | UI framework |
| **TypeScript** | 5.x | Type safety |
| **Pinia** | Latest | State management |
| **TipTap** | Latest | Rich text editor |
| **Tailwind** | 3.x | Styling |
| **Vue Router** | 4.x | Navigation |

</details>

---

## 🚀 Quick Start

### Prerequisites

> Docker 20+ and Docker Compose 2+ required

### One-Command Setup

```bash
# Clone and enter project
git clone git@github.com:jirniyjirniy/commenthub.git
cd commenthub

# Copy environment template
cp .env.example .env

# Launch all services
docker-compose up --build
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Frontend** | http://localhost | Vue.js SPA |
| 🔧 **Backend API** | http://localhost:8000 | Django REST |
| 📚 **API Docs** | http://localhost:8000/api/schema/swagger-ui/ | Swagger UI |
| 🗄️ **Admin Panel** | http://localhost:8000/admin/ | Django Admin |

---

## 🔧 Configuration

<details>
<summary><b>Environment Variables (.env file)</b></summary>

```env
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔐 SECURITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
PRODUCTION=False
ALLOWED_HOSTS=localhost,127.0.0.1

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 💾 DATABASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DB_NAME=comments_db
DB_USER=postgres
DB_PASSWORD=secure_password_here
DB_HOST=postgres
DB_PORT=5432

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ☁️ CLOUDINARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 RECAPTCHA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECAPTCHA_PUBLIC_KEY=your_public_key
RECAPTCHA_PRIVATE_KEY=your_private_key
VITE_RECAPTCHA_SITE_KEY=your_site_key

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 FRONTEND
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VITE_API_BASE_URL=/api
VITE_API_HOST=http://localhost:8000
```

</details>

---

## 📂 Project Structure

```
commnethub/
┣━━ 📁 app/                         # Main Django application
┃   ┣━━ 📁 migrations/             # Database migrations
┃   ┣━━ 📁 templates/              # HTML templates
┃   ┣━━ __init__.py
┃   ┣━━ admin.py                   # Django admin config
┃   ┣━━ apps.py                    # App configuration
┃   ┣━━ consumers.py               # WebSocket consumers
┃   ┣━━ exceptions.py              # Custom exceptions
┃   ┣━━ middleware.py              # Custom middleware
┃   ┣━━ models.py                  # Database models
┃   ┣━━ routing.py                 # WebSocket routing
┃   ┣━━ serializers.py             # DRF serializers
┃   ┣━━ signals.py                 # Django signals
┃   ┣━━ tasks.py                   # Celery tasks
┃   ┣━━ tests.py                   # Unit tests
┃   ┣━━ urls.py                    # URL routing
┃   ┣━━ utils.py                   # Utility functions
┃   ┗━━ views.py                   # API views
┃
┣━━ 📁 comments_api/               # Django project config
┃   ┣━━ __init__.py
┃   ┣━━ asgi.py                   # ASGI + WebSocket
┃   ┣━━ celery.py                 # Celery configuration
┃   ┣━━ celery_settings.py        # Celery settings
┃   ┣━━ settings.py               # Main settings
┃   ┣━━ urls.py                   # Root URL config
┃   ┗━━ wsgi.py                   # WSGI server
┃
┣━━ 📁 vue_ui/                     # Vue.js frontend
┃   ┣━━ 📁 public/                # Static assets
┃   ┣━━ 📁 src/
┃   ┃   ┣━━ 📁 api/               # API client
┃   ┃   ┣━━ 📁 components/        # Vue components
┃   ┃   ┣━━ 📁 config/            # Frontend config
┃   ┃   ┣━━ 📁 stores/            # Pinia stores
┃   ┃   ┣━━ 📁 types/             # TypeScript types
┃   ┃   ┣━━ 📁 utils/             # Utilities
┃   ┃   ┣━━ 📁 views/             # Page views
┃   ┃   ┣━━ 📁 router/            # Vue Router
┃   ┃   ┣━━ App.vue               # Root component
┃   ┃   ┣━━ index.css             # Global styles
┃   ┃   ┗━━ main.ts               # Entry point
┃   ┣━━ .gitignore
┃   ┣━━ Dockerfile
┃   ┣━━ index.html
┃   ┣━━ nginx.conf
┃   ┣━━ package.json
┃   ┣━━ package-lock.json
┃   ┣━━ tsconfig.json
┃   ┣━━ tsconfig.app.json
┃   ┣━━ tsconfig.node.json
┃   ┗━━ vite.config.ts
┃
┣━━ 📁 logs/                       # Application logs
┣━━ 📁 media/                      # User uploaded files
┣━━ 📁 static/                     # Django static files
┣━━ 📁 templates/                  # Global templates
┃
┣━━ .dockerignore
┣━━ .env                           # Environment variables
┣━━ .gitignore
┣━━ .python-version
┣━━ 🐳 docker-compose.yml          # Docker orchestration
┣━━ 🐳 Dockerfile                  # Backend container
┣━━ 📦 requirements.txt            # Python dependencies
┣━━ 🔧 manage.py                   # Django management
┗━━ 📖 README.md                   # This file
```

---

## 🔌 API Reference

### Authentication Endpoints

```http
POST   /api/register/              # Create new account
POST   /api/login/                 # Get JWT token
POST   /api/token/refresh/         # Refresh token
GET    /api/user/profile/          # Get current user
```

### Comments Endpoints

```http
GET    /api/comments/              # List all comments
POST   /api/comments/              # Create comment
GET    /api/comments/{id}/         # Get single comment
PUT    /api/comments/{id}/         # Update (owner only)
DELETE /api/comments/{id}/         # Delete (owner only)
GET    /api/comments/{id}/replies/ # Get nested replies
```

### WebSocket Endpoints

```ws
WS /ws/notifications/              # Real-time notifications
```

> **Interactive API Docs:** Visit http://localhost:8000/api/schema/swagger-ui/ for full documentation

---

## 💻 Development Guide

### Without Docker (Local Development)

#### Backend Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Setup database
uv run manage.py migrate
uv run manage.py createsuperuser

# Run development server
uv run uvicorn comments_api.asgi:application --reload --host 0.0.0.0 --port 8000

# In separate terminals:
uv run celery -A comments_api worker -l info
uv run celery -A comments_api beat -l info
```

#### Frontend Setup

```bash
cd vue_ui
npm install
npm run dev
```

### Testing

```bash
# Backend tests
uv run pytest --cov=apps --cov-report=html

# Frontend tests
cd vue_ui
npm run test:unit
npm run test:e2e
```

### Code Quality

```bash
# Backend linting
uv run ruff check .
uv run black .
uv run mypy .

# Frontend linting
cd vue_ui
npm run lint
npm run format
```

---

## 📊 Performance Features

- 🚀 **Redis caching** for frequently accessed data
- 📦 **Database indexing** on foreign keys
- ⚡ **Lazy loading** for nested comments
- 🔄 **Pagination** to limit response size
- 🎯 **Query optimization** with select_related/prefetch_related
- 📡 **WebSocket pooling** for real-time updates

---

## 🛡️ Security Features

| Feature | Implementation |
|---------|---------------|
| Authentication | JWT with refresh tokens |
| Password Hashing | Django Argon2 |
| CSRF Protection | Django middleware |
| XSS Prevention | HTML sanitization |
| SQL Injection | Django ORM |
| Rate Limiting | Django-ratelimit |
| File Validation | Size & type checks |
| HTTPS Ready | Production config |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Standards

- Write tests for new features
- Follow PEP 8 (Python) and ESLint (TypeScript)
- Update documentation
- Add type hints

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**jirniyjirniy**

- GitHub: [@jirniyjirniy](https://github.com/jirniyjirniy)

---

## 🙏 Acknowledgments

- Django & DRF communities
- Vue.js ecosystem
- TipTap editor team
- Cloudinary for media hosting
- All open-source contributors

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**[Report Bug](https://github.com/jirniyjirniy/commenthub/issues)** • 
**[Request Feature](https://github.com/jirniyjirniy/commenthub/issues)** • 
**[Documentation](http://localhost:8000/api/schema/swagger-ui/)**

Made with ❤️ by jirniyjirniy

</div>