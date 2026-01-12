"""
Настройки для запуска тестов
Используем локальный кеш вместо Redis для изоляции тестов
"""
from .settings import *

# ============================================
# ТЕСТОВАЯ БАЗА ДАННЫХ
# ============================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # База в памяти для быстрых тестов
    }
}

# ============================================
# ЛОКАЛЬНЫЙ КЕШ (НЕ REDIS)
# ============================================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

# ============================================
# CHANNEL LAYERS (В ПАМЯТИ)
# ============================================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# ============================================
# CELERY (СИНХРОННЫЙ РЕЖИМ ДЛЯ ТЕСТОВ)
# ============================================
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ============================================
# EMAIL (CONSOLE BACKEND ДЛЯ ТЕСТОВ)
# ============================================
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# ============================================
# ОТКЛЮЧАЕМ ВНЕШНИЕ СЕРВИСЫ
# ============================================
# reCAPTCHA будет мокироваться в тестах
RECAPTCHA_PRIVATE_KEY = "test-key"

# Cloudinary будет мокироваться в тестах
CLOUDINARY_CLOUD_NAME = "test-cloud"
CLOUDINARY_API_KEY = "test-key"
CLOUDINARY_API_SECRET = "test-secret"

# ============================================
# УСКОРЕНИЕ ТЕСТОВ
# ============================================
# Упрощаем хеширование паролей для ускорения
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Отключаем миграции (опционально, для еще большей скорости)
# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#     def __getitem__(self, item):
#         return None
# MIGRATION_MODULES = DisableMigrations()

# ============================================
# ЛОГИРОВАНИЕ (МИНИМАЛЬНОЕ)
# ============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}