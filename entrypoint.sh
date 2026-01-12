#!/bin/bash
set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting Django Application${NC}"
echo -e "${GREEN}========================================${NC}"

cd /app/backend

# 1. Ожидание доступности порта базы данных
wait_for_db() {
    echo -e "${YELLOW}⏳ Waiting for PostgreSQL port...${NC}"
    while ! pg_isready -h ${DB_HOST:-postgres} -p ${DB_PORT:-5432} -U ${DB_USER:-postgres}; do
        echo -e "${YELLOW}   PostgreSQL is unavailable - sleeping${NC}"
        sleep 1
    done
    echo -e "${GREEN}✅ PostgreSQL port is ready!${NC}"
}

# 2. Ожидание готовности таблиц (нужно для Celery Beat/Worker)
wait_for_migrations() {
    echo -e "${YELLOW}⏳ Waiting for migrations to complete...${NC}"
    until python manage.py check --database default > /dev/null 2>&1; do
      echo -e "${YELLOW}   Migrations are not ready yet - sleeping${NC}"
      sleep 2
    done
    echo -e "${GREEN}✅ Migrations are ready!${NC}"
}

# 3. Запуск миграций в правильном порядке
run_migrations() {
    echo -e "${YELLOW}🔄 Checking and running migrations...${NC}"
    python manage.py makemigrations users --noinput
    python manage.py makemigrations comments --noinput
    python manage.py migrate users --noinput
    python manage.py migrate --noinput
}

collect_static() {
    echo -e "${YELLOW}📦 Collecting static files...${NC}"
    python manage.py collectstatic --noinput --clear
}

create_superuser() {
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
        echo -e "${YELLOW}👤 Checking superuser...${NC}"
        python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print("✅ Superuser created!")
else:
    print("ℹ️ Superuser exists")
END
    fi
}

MODE=${1:-server}

case "$MODE" in
    server)
        echo -e "${GREEN}🚀 Mode: $MODE (Daphne ASGI)${NC}"
        wait_for_db
        run_migrations
        collect_static
        create_superuser
        # ИСПОЛЬЗУЕМ DAPHNE ДЛЯ WEBSOCKET!
        exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
        ;;
    
    gunicorn)
        echo -e "${GREEN}🚀 Mode: $MODE${NC}"
        wait_for_db
        run_migrations
        collect_static
        create_superuser
        exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
        ;;
    
    celery_worker)
        echo -e "${GREEN}⚙️ Mode: celery_worker${NC}"
        wait_for_db
        wait_for_migrations
        exec celery -A config worker --loglevel=info
        ;;
    
    celery_beat)
        echo -e "${GREEN}⚙️ Mode: celery_beat${NC}"
        wait_for_db
        wait_for_migrations
        rm -f celerybeat-schedule
        exec celery -A config beat --loglevel=info
        ;;
    
    *)
        echo -e "${RED}❌ Unknown mode: $MODE${NC}"
        exit 1
        ;;
esac
