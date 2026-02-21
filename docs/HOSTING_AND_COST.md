# Hosting Options and Cost Comparison

**Author:** Victor.I

Quick comparison: AWS vs Vercel, tools that reduce manual config, and free/cheap hosting for AI QueryLens (Next.js + Django + Node).

---

## 1. AWS Tools That Reduce Manual Config

| Tool | What it does | Manual config |
|------|----------------|----------------|
| **AWS Toolkit (Cursor/VS Code)** | Sign in with AWS (browser or IAM). Create Amplify app from IDE, deploy from GUI. | One-time: install extension, connect AWS account. Then use "AWS: Create New App" and follow prompts. Backend (Django/Node) still needs ECR + App Runner or ECS once. |
| **AWS Amplify Console** | Connect GitHub repo; Amplify builds and deploys the frontend. | Connect repo, set root to `frontend`, add env vars. No CLI if you use the Console only. |
| **AWS Copilot** | CLI that generates and deploys containers (App Runner or ECS) from a simple app name and type. | One-time: `copilot init`, answer prompts. It generates the config; you run `copilot deploy`. |
| **AWS Serverless Application Model (SAM)** | For Lambda + API Gateway, not for long-running Django/Node. | Not a good fit for this stack without rewriting backends. |

**Recommendation for least manual on AWS:** Use **AWS Toolkit** to sign in and create the Amplify app (frontend). For Django and Node, either use the **AWS Console** once (App Runner > Create service > ECR image) or **AWS Copilot** so the CLI generates the deployment config.

---

## 2. AWS vs Vercel – Which Is Cheaper?

This project has **three parts:** Next.js frontend, Django API, Node WebSocket server.

| | AWS (your current plan) | Vercel |
|--|-------------------------|--------|
| **Frontend (Next.js)** | Amplify: free tier, then paid. | **Vercel:** Free hobby tier (generous). |
| **Backend (Django + Node)** | App Runner (or ECS): always-on, ~$35–65+/month. | **Vercel does not run Django or long-lived Node WS.** You must host them elsewhere (see free options below). |
| **Total** | ~$35–130/month (Amplify + App Runner x2 + optional EC2 for Ollama). | **Frontend on Vercel: $0.** Backend elsewhere: $0–25/month (free tiers or cheap). |

**Verdict:** For this full stack, **Vercel (frontend only) + a free/cheap backend host is usually cheaper** than running everything on AWS. AWS is cheaper only if you already have credits or use free tier carefully (e.g. one small App Runner + Amplify free tier).

---

## 3. Free or Very Cheap Hosting for This Stack

### Frontend (Next.js) – free

| Provider | Free tier | Notes |
|----------|-----------|--------|
| **Vercel** | Yes | Connect GitHub, set root to `frontend`. Easiest for Next.js. |
| **Netlify** | Yes | Similar: connect repo, build command `npm run build`, publish `.next` or use Next runtime. |
| **Cloudflare Pages** | Yes | Supports Next.js (adapter). |
| **AWS Amplify** | Free tier | 1000 build min/month, 15 GB served; enough for small traffic. |

### Backend (Django + Node) – free or cheap

| Provider | Free tier | Notes |
|----------|-----------|--------|
| **Render** | Yes (spins down after idle) | Two services: one for Django (Python), one for Node. Free tier sleeps; cold start on first request. |
| **Railway** | Limited free credit/month | Connect repo, add Django and Node services (or Docker). Easiest “all-in-one” for backend. |
| **Fly.io** | Small free allowance | Run Docker; deploy Django and Node as two apps. |
| **Google Cloud Run** | Free tier per month | Pay per request; can run Django and Node in containers. Free tier often enough for demos. |
| **PythonAnywhere** | Free tier | Django only; no Node. Good for API only; you’d need another free host for Node WS. |

### Easiest “almost free” full stack

1. **Frontend:** Vercel (connect GitHub, root = `frontend`, add `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_WS_URL`).
2. **Backend:** **Render** – create a Web Service for Django (build: `pip install -r backend/requirements.txt`, start: `gunicorn` or `python backend/manage.py runserver`), and a second Web Service for Node. Set env vars; use Render URLs in Vercel env.
3. Or **Railway** – one project, two services from the same repo (Django + Node). Use Railway URLs in Vercel.

---

## 4. Summary

- **Least manual on AWS:** **AWS Toolkit** (sign in, create Amplify app) + one-time App Runner setup for Django and Node (or **AWS Copilot** to generate that).
- **Cheaper:** **Vercel (frontend)** + **Render or Railway (backend)** is usually cheaper than full AWS for this stack.
- **Free hosting:** Frontend on **Vercel/Netlify/Cloudflare**. Backend on **Render** or **Railway** free tier (with cold starts) or **Fly.io** / **Cloud Run** free allowance.

For a portfolio or recruiter demo, **Vercel + Render** (or Railway) is often the fastest and cheapest path with minimal manual config.
