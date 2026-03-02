# AWS Deployment Checklist

**Author:** Victor.I

Quick checklist for deploying AI QueryLens to AWS.

## Deployment progress

| Step | Status | Notes |
|------|--------|--------|
| Pre-deployment (CLI, Docker, Toolkit) | | |
| Build & push images to ECR | | Run `./scripts/deploy-aws.sh us-east-1` |
| Deploy Django API (App Runner) | | Port 8000, health `/api/health/`, SECRET_KEY, DEBUG=0 |
| Deploy Node WS (App Runner) | | |
| Deploy frontend (Amplify) | | |
| Update CORS / test | | |

## Pre-Deployment

- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] AWS Toolkit installed in VS Code/Cursor
- [ ] Docker installed and running
- [ ] Git repository connected (for Amplify)

## Step 1: Ollama (Optional - can skip initially)

- [ ] Launch EC2 instance (t3.medium or larger, Amazon Linux 2)
- [ ] Use `scripts/setup-ollama-ec2.sh` as user data
- [ ] Configure security group: allow inbound port 11434 from App Runner/ECS
- [ ] Note private IP: `_________________`

## Step 2: Build & Push Images

- [ ] Run: `./scripts/deploy-aws.sh us-east-1`
- [ ] Verify images in ECR Console

## Step 3: Deploy Django API

- [ ] AWS Console → App Runner → Create service
- [ ] Source: ECR → `querylens-api:latest`
- [ ] Service name: `querylens-api`
- [ ] Port: `8000` (container entrypoint reads `PORT` from env; use 8000 in App Runner config)
- [ ] CPU/Memory: 1 vCPU, 2 GB
- [ ] Environment variables (from `.env.aws`):
  - [ ] `SECRET_KEY` (generate with Python command)
  - [ ] `DEBUG=0`
  - [ ] `ALLOWED_HOSTS` (add App Runner URL after creation)
  - [ ] `CORS_ALLOWED_ORIGINS` (add Amplify URL after creation)
  - [ ] `OLLAMA_BASE_URL` (if using Ollama)
  - [ ] `OLLAMA_MODEL=llama3.2`
- [ ] Deploy and note URL: `_________________`

## Step 4: Deploy Node WebSocket

- [ ] AWS Console → App Runner → Create service
- [ ] Source: ECR → `querylens-ws:latest`
- [ ] Service name: `querylens-ws`
- [ ] Port: `3001`
- [ ] CPU/Memory: 0.25 vCPU, 0.5 GB
- [ ] Environment variables:
  - [ ] `DJANGO_API_URL` (from Step 3)
- [ ] Deploy and note URL: `_________________`

## Step 5: Deploy Frontend (Amplify)

### Option A: AWS Toolkit
- [ ] Command Palette → "AWS: Create New App"
- [ ] Choose Amplify → Host web app
- [ ] Connect repository
- [ ] Set root directory: `frontend`
- [ ] Build command: `npm ci && npm run build`

### Option B: AWS Console
- [ ] Amplify → New app → Connect repository
- [ ] Select repo and branch
- [ ] Monorepo: Yes, root = `frontend`
- [ ] Build settings: auto-detected (Next.js)

### Environment Variables
- [ ] `NEXT_PUBLIC_API_URL` (from Step 3)
- [ ] `NEXT_PUBLIC_WS_URL` (from Step 4, use `wss://`)
- [ ] Deploy and note URL: `_________________`

## Step 6: Update Backend CORS

- [ ] Go back to Django App Runner service
- [ ] Update environment variables:
  - [ ] `ALLOWED_HOSTS` - add Amplify URL
  - [ ] `CORS_ALLOWED_ORIGINS` - add Amplify URL
- [ ] Redeploy service

## Step 7: Test

- [ ] Open Amplify URL in browser
- [ ] Upload a CSV file
- [ ] Ask a question in chat
- [ ] Verify WebSocket connection works
- [ ] Check analytics pages load

## Estimated Costs (Monthly)

- **App Runner (Django):** ~$25-50 (1 vCPU, 2GB, always on)
- **App Runner (Node):** ~$10-15 (0.25 vCPU, 0.5GB)
- **Amplify:** ~$0-5 (free tier covers most usage)
- **ECR:** ~$1 (storage for 2 images)
- **EC2 (Ollama):** ~$30-60 (t3.medium, on-demand)
- **Total:** ~$66-131/month

## Optimization Tips

- Use EC2 Spot for Ollama (save 70%)
- Use App Runner auto-scaling (pay only for usage)
- Enable CloudFront for Amplify (better performance)
- Use RDS for production database (instead of SQLite)

## Troubleshooting: Django container not starting

- **Port:** The container entrypoint binds to `$PORT` (default 8000). In App Runner, set the port to `8000` so it matches.
- **Required env:** Set at least `SECRET_KEY` and `DEBUG=0`. If `ALLOWED_HOSTS` is missing, the app allows `.awsapprunner.com` when `DEBUG=0`.
- **Logs:** In App Runner → your service → Logs, check the latest deployment log. Look for:
  - `ModuleNotFoundError` or `ImportError` → rebuild image with `backend/` and `src/` present; ensure `PYTHONPATH=/app`.
  - `OperationalError` (SQLite) → migrations run in entrypoint; if the filesystem is read-only, the app may fail (use RDS or a writable volume in production).
  - Gunicorn "Listening at" → app started; if health check still fails, confirm the health URL is `https://<your-url>/api/health/` and returns 200.
- **Health check path:** Use `/api/health/` (with trailing slash). The root `/` is not routed.

## Support

Issues? Check `docs/aws-deploy-with-toolkit.md` for detailed instructions.
