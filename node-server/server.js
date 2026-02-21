/**
 * Victor.I - WebSocket server for AI Analytics.
 * Proxies query messages to Django API and sends responses back over WS.
 */
const http = require('http');
const { WebSocketServer } = require('ws');

const PORT = parseInt(process.env.NODE_WS_PORT || '3001', 10);
const DJANGO_API_URL = process.env.DJANGO_API_URL || 'http://localhost:8000';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('WebSocket server for AI Analytics. Connect via WS.\n');
});

const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  ws.on('message', async (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw.toString());
    } catch {
      ws.send(JSON.stringify({ type: 'error', error: 'Invalid JSON' }));
      return;
    }
    if (msg.type === 'query' && msg.dataset_id && msg.question) {
      try {
        const res = await fetch(`${DJANGO_API_URL}/api/query/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dataset_id: msg.dataset_id,
            question: msg.question,
          }),
        });
        const data = await res.json();
        ws.send(JSON.stringify({
          type: 'response',
          answer: data.answer,
          chart_data: data.chart_data || null,
          confidence: data.confidence,
        }));
      } catch (err) {
        ws.send(JSON.stringify({
          type: 'error',
          error: err.message || 'Django request failed',
        }));
      }
    } else {
      ws.send(JSON.stringify({ type: 'error', error: 'Expected { type: "query", dataset_id, question }' }));
    }
  });
});

server.listen(PORT, () => {
  console.log(`WS server listening on port ${PORT}. Django API: ${DJANGO_API_URL}`);
});
