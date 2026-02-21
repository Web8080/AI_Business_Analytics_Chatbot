# Victor.I - WebSocket server for QueryLens. Build from repo root: docker build -f node-server/Dockerfile .
FROM node:20-alpine
WORKDIR /app
COPY node-server/package*.json ./
RUN npm ci --omit=dev
COPY node-server/ ./
EXPOSE 3001
CMD ["node", "server.js"]
