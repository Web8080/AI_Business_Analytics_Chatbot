# Victor.I - Django API for QueryLens. Build from repo root: docker build -f backend/Dockerfile .
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt gunicorn
COPY backend/ ./backend/
COPY src/ ./src/
COPY config.py ./
WORKDIR /app/backend
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "backend.wsgi:application"]
