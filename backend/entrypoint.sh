#!/bin/bash
# Victor.I - App Runner / container entrypoint: migrations, uploads dir, then gunicorn on PORT.
set -e
cd /app/backend
export PYTHONPATH=/app

# Ensure upload directory exists (views use REPO_ROOT/data/uploads)
mkdir -p /app/data/uploads

# Apply migrations so auth/contenttypes tables exist
python manage.py migrate --noinput

# App Runner injects PORT; default 8000 for local Docker
PORT="${PORT:-8000}"
exec gunicorn --bind "0.0.0.0:${PORT}" --workers 2 --timeout 120 backend.wsgi:application
