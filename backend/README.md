# AI Analytics - Django Backend

**Author:** Victor.I

Primary REST API for the AI Analytics Intelligence System: CSV upload, schema preview, natural-language query, and chart data. Dataset store is in-memory (suitable for dev; use DB or cache in production).

## Install

```bash
pip install -r requirements.txt
```

Ensure the repo root has `src/` (data_ingestion, data_cleaning, conversational) and optional `.env` (e.g. `OPENAI_API_KEY`).

## Run

From **repo root** (so `src/` is importable):

```bash
cd /path/to/AI_Analytics_Intelligence_System_with_Conversational_Interface
pip install -r backend/requirements.txt
python backend/manage.py migrate
PYTHONPATH=. python backend/manage.py runserver
```

If port 8000 is in use, run on another port:

```bash
PYTHONPATH=. python backend/manage.py runserver 8080
```

Then set `NEXT_PUBLIC_API_URL=http://localhost:8080` in the frontend env.

Or from this directory if `src` is on the path:

```bash
python manage.py migrate
python manage.py runserver
```

API base: `http://localhost:8000`. Endpoints: `POST /api/upload/csv/`, `POST /api/query/`, `GET /api/datasets/`, `GET /api/datasets/<id>/preview/`, `GET /api/health/`.

## Env (optional)

- `SECRET_KEY` – Django secret
- `DEBUG` – 1 for dev
- `ALLOWED_HOSTS` – comma-separated
- `CORS_ALLOWED_ORIGINS` – e.g. `http://localhost:3000`
- `OPENAI_API_KEY` – for NL query (optional; fallback used if missing)
