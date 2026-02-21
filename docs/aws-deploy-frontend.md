# AWS Frontend Deployment (S3 + CloudFront or Amplify)

**Author:** Victor.I

Deploy the Next.js AI Analytics dashboard to AWS. Easiest options: **Amplify** (recommended) or **S3 + CloudFront**.

## Option 1: AWS Amplify

1. In AWS Amplify Console, connect your Git repository (GitHub/GitLab/Bitbucket).
2. Select the repo and branch. Set root directory to project root (or leave default).
3. Build settings:
   - **App:** Monorepo; set **Root directory** to `frontend` if the app lives in `frontend/`.
   - **Build command:** `npm ci && npm run build`
   - **Output directory:** `.next` (Amplify detects Next.js) or use default.
4. Environment variables (Amplify Console > App settings > Environment variables):
   - `NEXT_PUBLIC_API_URL` = your production Django API URL (e.g. `https://api.yourdomain.com`)
   - `NEXT_PUBLIC_WS_URL` = your production Node WebSocket URL (e.g. `wss://ws.yourdomain.com`)
5. Save and deploy. Amplify will build and host the app with HTTPS and a default URL.

For **static export** (no server-side rendering), add to `frontend/next.config.js`:

```js
const nextConfig = {
  output: 'export',
};
```

Then output directory in Amplify is `out`.

## Option 2: S3 + CloudFront (static export)

1. In `frontend/next.config.js`, set `output: 'export'`. Run `npm run build`; Next.js will write static files to `frontend/out/`.
2. Create an S3 bucket (e.g. `ai-analytics-dashboard`). Enable static website hosting (optional; CloudFront will use the bucket as origin).
3. Upload the contents of `frontend/out/` to the bucket (e.g. `aws s3 sync frontend/out s3://your-bucket/ --delete`).
4. Create a CloudFront distribution:
   - Origin: S3 bucket (or S3 website endpoint if you enabled static hosting).
   - Default root object: `index.html`.
   - Error pages: 403 and 404 -> `/index.html` with 200 (for client-side routing).
5. Set env at build time: `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_WS_URL` must be set when running `npm run build` so they are inlined (e.g. in CI or locally before upload).

## Backend (Django and Node)

- **Django:** Deploy to AWS App Runner, ECS Fargate, or EC2. Use RDS for DB and S3 for uploads in production. Set `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` to your frontend origin.
- **Node (WebSocket):** Deploy to ECS Fargate, App Runner, or EC2. Set `DJANGO_API_URL` to the production Django URL. Ensure the frontend `NEXT_PUBLIC_WS_URL` points to this service (e.g. wss://ws.yourdomain.com).
