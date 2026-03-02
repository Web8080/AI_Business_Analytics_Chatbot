# Deploy to Render.com (FREE)

**Author:** Victor.I

## Environment variables to set on Render

### Django API (Web Service)

| Key | Required | Example / notes |
|-----|----------|------------------|
| `SECRET_KEY` | Yes | Random string, e.g. `python3 -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | Yes | `0` for production |
| `ALLOWED_HOSTS` | Yes | `*` or your Render URL host, e.g. `querylens-api.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | Yes | Frontend URL(s), e.g. `https://your-frontend.onrender.com` or `*` for testing |
| `OPENAI_API_KEY` | No | Leave blank to use Ollama or rule-based fallback |
| `OLLAMA_BASE_URL` | No | Only if using Ollama, e.g. `http://your-ollama-host:11434` |
| `OLLAMA_MODEL` | No | e.g. `llama3.2` |

Render sets `PORT` automatically; the container entrypoint uses it.

### Node WebSocket (if you add a second Web Service)

| Key | Required | Example / notes |
|-----|----------|------------------|
| `DJANGO_API_URL` | Yes | Your Django service URL, e.g. `https://querylens-api.onrender.com` |

Render sets `PORT`; the Node server should listen on `process.env.PORT || 3001`.

### Next.js frontend (if you deploy it on Render)

| Key | Required | Example / notes |
|-----|----------|------------------|
| `NEXT_PUBLIC_API_URL` | Yes | Django API URL, e.g. `https://querylens-api.onrender.com` |
| `NEXT_PUBLIC_WS_URL` | No (if no WS) | Node WS URL, e.g. `wss://querylens-ws.onrender.com` |

---

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Deploy on Render

Use **Dockerfile path: backend/Dockerfile** so the Django API runs (Ollama support, no OpenAI required). The root `Dockerfile` runs the legacy FastAPI app and does not support Ollama.

1. Go to: https://render.com
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Connect your repository
5. Settings:
   - **Name:** querylens-api
   - **Environment:** Docker
   - **Dockerfile Path:** `backend/Dockerfile` (required for Ollama support; do not use the root Dockerfile)
   - **Instance Type:** Free
   - **Health Check Path:** `/api/health/`
6. Add environment variables:
   - `SECRET_KEY` = (generate random string)
   - `DEBUG` = 0
   - `ALLOWED_HOSTS` = *
   - `CORS_ALLOWED_ORIGINS` = *
7. Click **Create Web Service**

## Step 3: Wait 5 minutes

Render will:
- Build your Docker image
- Deploy automatically
- Give you a URL: `https://querylens-api.onrender.com`

## Cost: $0/month (FREE tier)

Your site will be live at the Render URL!
