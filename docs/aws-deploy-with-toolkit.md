# Deploy AI QueryLens to AWS Using AWS Toolkit

**Author:** Victor.I

Use the **AWS Toolkit** (in VS Code/Cursor) and **AWS CLI** to deploy the frontend, Django backend, and Node WebSocket server. Ollama can run on an EC2 instance for production.

---

## Prerequisites

- **AWS Toolkit** installed (Cursor/VS Code: Extensions > search "AWS Toolkit").
- **AWS CLI** installed and configured (`aws configure` with access key, secret, region).
- **Docker** (optional but recommended for App Runner / ECS).

---

## 1. Frontend (Next.js) – Amplify via Toolkit or CLI

### Option A: AWS Toolkit (GUI)

1. Open **Command Palette** (Cmd+Shift+P / Ctrl+Shift+P) and run **AWS: Create New App** or go to **AWS** in the sidebar.
2. Choose **Amplify** > **Host web app**.
3. When prompted:
   - **Repository:** Connect your Git provider (GitHub/GitLab/etc.) and select this repo, or choose "Deploy without Git" and use a zip later.
   - **Branch:** e.g. `main`.
   - **Monorepo:** Yes. Set **Root directory** to `frontend`.
   - **Build:** Build command `npm ci && npm run build` (or `npm install && npm run build`). Output is `.next` (Amplify detects Next.js).
4. In Amplify Console (open from Toolkit or AWS Console):
   - **App settings > Environment variables** – add:
     - `NEXT_PUBLIC_API_URL` = your production Django URL (you’ll get this after deploying the backend).
     - `NEXT_PUBLIC_WS_URL` = your production Node WS URL (after deploying Node).
5. Save and deploy. Amplify gives you a URL like `https://main.xxxxx.amplifyapp.com`.

### Option B: AWS CLI (no Toolkit)

```bash
# Install Amplify CLI if you prefer: npm install -g @aws-amplify/cli
# Or use Console: Amplify > New app > Connect repository > set root to frontend
```

Use the AWS Console (Amplify > New app > Connect repository) and set **Root directory** to `frontend`, then add the same env vars as above.

---

## 2. Backend (Django) – App Runner or ECS via Toolkit/CLI

Django must run in a container or on a server. Two simple options:

### Option A: AWS App Runner (easiest from Toolkit/CLI)

1. **Add a Dockerfile for Django** (see below).
2. Push the image to **Amazon ECR** (Toolkit: AWS > ECR > Create repository, then push; or use CLI).
3. **App Runner:** In AWS Console go to App Runner > Create service:
   - Source: ECR → select your Django image.
   - Service name: e.g. `querylens-api`.
   - CPU/Memory: 1 vCPU, 2 GB.
   - Environment variables: add `SECRET_KEY`, `DEBUG=0`, `ALLOWED_HOSTS` (include your App Runner URL), `CORS_ALLOWED_ORIGINS` (your Amplify/frontend URL), `OLLAMA_BASE_URL` (your Ollama server URL in prod), `OLLAMA_MODEL=llama3.2`.
4. Note the App Runner URL (e.g. `https://xxxxx.us-east-1.awsapprunner.com`) and use it as `NEXT_PUBLIC_API_URL` in Amplify.

### Option B: ECS Fargate

1. Build and push Django image to ECR.
2. In Toolkit: **AWS > ECS > Create cluster** (or use Console).
3. Create a **Task Definition** (Fargate, add your Django image, set env vars as above).
4. Create an **Application Load Balancer** and an **ECS Service** that uses the task definition. Expose the ALB URL as your API URL.

### Django Dockerfile (for App Runner / ECS)

Use the existing `backend/Dockerfile`. Build from **repo root** so `backend/` and `src/` are available:

```bash
cd /path/to/AI_Analytics_Intelligence_System_with_Conversational_Interface
docker build -f backend/Dockerfile -t querylens-api .
```

---

## 3. Node (WebSocket) – App Runner or ECS

Same idea as Django: containerize, push to ECR, run on App Runner or ECS.

1. **Add `node-server/Dockerfile`** (see below).
2. Push to ECR, then create an App Runner service (or ECS service) with env `DJANGO_API_URL` = your Django production URL.
3. Note the Node service URL and set `NEXT_PUBLIC_WS_URL` in Amplify to the **WebSocket** URL (e.g. `wss://xxxxx.awsapprunner.com` if App Runner supports WS, or the ALB/URL for your Node service). App Runner supports WebSockets; use the same URL with `wss://` if HTTPS.

### Node Dockerfile

Use the existing `node-server/Dockerfile`. Build from **repo root**:

```bash
docker build -f node-server/Dockerfile -t querylens-ws .
```

---

## 4. Ollama in Production

- Run Ollama on an **EC2** instance (e.g. Amazon Linux 2): install Ollama, run `ollama serve` and `ollama run llama3.2`.
- Set **Security group** so your Django (App Runner/ECS) can reach the EC2 IP on port 11434.
- In Django (and Node if it calls Ollama) env: `OLLAMA_BASE_URL=http://<ec2-private-ip>:11434`.

---

## 5. Order of Deployment

1. **Ollama (optional for day one):** EC2 + Ollama; note the URL.
2. **Django:** Build image, ECR, App Runner (or ECS). Set `OLLAMA_BASE_URL` if Ollama is ready. Note API URL.
3. **Node:** Build image, ECR, App Runner (or ECS). Set `DJANGO_API_URL` = Django URL. Note WS URL.
4. **Frontend (Amplify):** Connect repo, root `frontend`, set `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_WS_URL`. Deploy.
5. **Update Django:** Set `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` to include Amplify URL and your domain if any.

---

## 6. Toolkit Shortcuts

- **AWS Explorer:** View regions, Lambda, ECR, Amplify apps.
- **Deploy to App Runner:** Right‑click a Dockerfile or use "AWS: Deploy to App Runner" if available.
- **Amplify:** "AWS: Amplify - Deploy app" or open Amplify in browser from Toolkit.
- **Credentials:** "AWS: Connect to AWS" or configure in `~/.aws/credentials`.

---

## 7. Automated Deployment Script

Use the provided script to automate Docker builds and ECR pushes:

```bash
# Configure AWS CLI first
aws configure

# Run automated deployment
./scripts/deploy-aws.sh us-east-1

# Or specify account ID explicitly
./scripts/deploy-aws.sh us-east-1 123456789012
```

The script will:
- Login to ECR
- Create ECR repositories
- Build Django and Node Docker images
- Push images to ECR
- Display next steps for App Runner and Amplify

## 8. Environment Variables

See `.env.aws` for a complete template of environment variables needed for each service.

**Generate Django SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## 9. Quick CLI Reference

```bash
# Configure CLI once
aws configure

# Manual ECR push (if not using script)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
aws ecr create-repository --repository-name querylens-api --region us-east-1
docker build -f backend/Dockerfile -t querylens-api .
docker tag querylens-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/querylens-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/querylens-api:latest

# Amplify: create app (then add env vars in Console)
aws amplify create-app --name querylens --region us-east-1
# Connect branch and set root via Console or amplify init
```

After Toolkit is installed, use **AWS** in the sidebar and the **Command Palette** to create and deploy Amplify apps and to work with ECR/App Runner/ECS.

---

## Troubleshooting

**Docker build fails:**
- Ensure you're building from repo root: `cd /path/to/AI_Analytics_Intelligence_System_with_Conversational_Interface`
- Check Docker is running: `docker ps`

**ECR push fails:**
- Verify AWS credentials: `aws sts get-caller-identity`
- Check region matches: `aws configure get region`

**App Runner can't reach Ollama:**
- Verify EC2 security group allows inbound on port 11434 from App Runner
- Use EC2 private IP, not public IP
- Test from App Runner: `curl http://<ec2-ip>:11434/api/tags`

**Frontend can't reach backend:**
- Check CORS settings in Django include Amplify URL
- Verify `NEXT_PUBLIC_API_URL` in Amplify env vars
- Check App Runner service is running and healthy
