# Customer Management Portal

A full-stack customer management portal built with React, TypeScript, Vite, FastAPI, SQLite, Docker, and test automation.

## Run locally

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000` by default.

## Run tests

```bash
cd backend
pytest
```

## Run with Docker

```bash
docker compose up --build
```

The frontend will be available at `http://localhost:5173` and the API at `http://localhost:8000`.
