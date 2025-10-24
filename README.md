# ROS2 Bags Recorder – Live Status Dashboard

A reference implementation of an offline-first ROS2 recording, edge sync, and live monitoring stack.

## Overview
This repository contains three services and a small library:
- Recorder (Python/rclpy): Discovers topics, buffers and segments data, emits telemetry, and manages recovery.
- Edge Server (FastAPI): Accepts segments, indexes sessions, exposes metrics and WebSocket events, and manages an upload queue.
- Sync Engine (Python library): Chunked, resumable uploads with basic de-duplication and conflict handling.
- Dashboard (React + Vite): Live status UI for sessions, metrics, alerts, and logs.

## Repository structure
```
.
├─ recorder/
│  ├─ src/
│  │  ├─ buffer.py
│  │  ├─ config.py
│  │  ├─ discovery.py
│  │  ├─ manifest.py
│  │  ├─ node.py
│  │  ├─ storage.py
│  │  ├─ telemetry.py
│  │  └─ recovery.py
│  └─ requirements.txt
├─ edge_server/
│  ├─ src/
│  │  ├─ config.py
│  │  ├─ index.py
│  │  ├─ metrics.py
│  │  ├─ queue.py
│  │  ├─ server.py
│  │  ├─ storage.py
│  │  └─ websocket.py
│  │  └─ sync.py
│  └─ requirements.txt
├─ sync_engine/
│  └─ src/
│     ├─ engine.py
│     ├─ uploader.py
│     ├─ deduplication.py
│     ├─ conflict.py
│     └─ recovery.py
├─ dashboard/
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ src/
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ public/
│  │  └─ index.html
│  └─ nginx.conf
├─ config/
│  ├─ recorder_config.yaml
│  ├─ edge_server_config.yaml
│  └─ dashboard_config.yaml
├─ Dockerfile.recorder
├─ Dockerfile.edge_server
├─ Dockerfile.dashboard
├─ docker-compose.yml
├─ .env.example
└─ .gitignore
```

## Exposed ports
- Dashboard (Nginx): 3000/tcp (container 80)
- Edge Server HTTP (FastAPI): 8080/tcp
- Edge Server WebSocket: 8765/tcp
- Edge Server metrics (Prometheus): 9091/tcp
- Recorder metrics: 9090/tcp (recorder runs with network_mode: host)

## Prerequisites
- Docker and Docker Compose
- Linux host recommended (recorder uses `network_mode: host`)
- ROS2 (on the host) for live topic discovery if you plan to integrate the recorder with a running ROS2 graph

## Quick start (Docker Compose)
1) Clone and enter the repo
```bash
git clone https://github.com/Maahir-AI-Robo/ROS2_BAGS-RECORDER-LIVE-STATUS-DASHBOARD.git
cd ROS2_BAGS-RECORDER-LIVE-STATUS-DASHBOARD
```
2) Create your environment file
```bash
cp .env.example .env
# Edit .env with your secrets (e.g., CLOUD_AUTH_TOKEN)
```
3) Review configuration
- Recorder: [config/recorder_config.yaml](config/recorder_config.yaml)
- Edge server: [config/edge_server_config.yaml](config/edge_server_config.yaml)
- Dashboard: [config/dashboard_config.yaml](config/dashboard_config.yaml)

4) Build and run
```bash
docker compose up -d --build
```
5) Open the dashboard
- http://localhost:3000

## Local development (without Docker)
- Edge server (FastAPI):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r edge_server/requirements.txt
uvicorn edge_server.src.server:app --host 0.0.0.0 --port 8080
```
- Dashboard (Vite):
```bash
cd dashboard
npm install
npm run start
```
- Recorder and Sync Engine are plain Python modules; wire them into your ROS2 environment and processes as needed.

## Configuration
- Environment variables (see [.env.example](.env.example))
  - RECORDER_ENCRYPTION_KEY: Optional encryption key for at-rest data
  - CLOUD_AUTH_TOKEN: Bearer token for cloud endpoint if used
  - BACKEND_URL, WS_URL: Dashboard connection targets
- YAML configs
  - recorder_config.yaml: discovery, QoS, buffering, storage, session, telemetry
  - edge_server_config.yaml: server, storage, queue, cloud, telemetry
  - dashboard_config.yaml: backend URLs, UI, alerts, defaults

## Status and roadmap
- This repository includes working service skeletons and reference flows for discovery, buffering, storage, indexing, queueing, and chunked uploads.
- Replace placeholders (e.g., actual ROS2 subscription/recording loop, real upload endpoints, checksumming/verification) as you integrate with your systems.

## Troubleshooting
- Ports already in use: adjust mappings in docker-compose.yml
- Permissions on data directories: ensure the host `./data/*` paths are writable
- Dashboard blank page: ensure the edge server is running and BACKEND_URL/WS_URL are reachable from the browser

## License
MIT (add a LICENSE file if required by your policies)