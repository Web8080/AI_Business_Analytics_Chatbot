# AI Analytics - Node WebSocket Server

**Author:** Victor.I

Single-purpose WebSocket server for streaming AI Analytics chat. Clients send `{ type: "query", dataset_id, question }`; server calls Django `/api/query/` and returns `{ type: "response", answer, chart_data, confidence }`.

## Install and run

```bash
npm install
npm run dev
```

Listens on port 3001 by default.

## Env

- `NODE_WS_PORT` – port (default 3001)
- `DJANGO_API_URL` – Django API base (default http://localhost:8000)
