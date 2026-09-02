# PROK — Predictive and Responsible Operations For Knowledge

PROK is an AI-powered College Personal Guide that helps students **manage → guide → support → grow** through one connected experience.

This repository contains the project foundation: runnable mobile, web, and API shells plus local MongoDB configuration. Product features are intentionally deferred.

## Product principles

- Build a realistic hackathon MVP before adding enterprise complexity.
- AI explains, guides, and personalizes; it never invents records or makes consequential decisions.
- Teachers and administrators remain responsible for attendance, eligibility, approvals, and policy decisions.
- Use deterministic rules for database-backed facts, thresholds, and workflow state.
- Do not represent demo data as real university data or claim unverified accuracy or pilot outcomes.

## Planned platform architecture

```text
Flutter mobile app ─┐
                    ├─> FastAPI backend ─> MongoDB
React web dashboard ─┘           │
                                └─> modular AI / recommendation services
```

Detailed scope, data model, API direction, security boundaries, and delivery phases are in [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md).

## Repository layout

```text
PROK/
├── backend/       # FastAPI, Pydantic models, MongoDB repositories, tests
├── mobile/        # Flutter student-first mobile client
├── web/           # React + Vite + TypeScript dashboard
├── ai/            # Optional, replaceable AI interfaces and adapters
├── database/      # MongoDB index definitions and data utilities
├── docs/          # Architecture, decisions, API and demo documentation
└── docker-compose.yml
```

## Run locally

### Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- Flutter SDK
- Docker Desktop

### Start MongoDB

```powershell
docker compose up -d mongodb
```

### Start the API

```powershell
cd backend
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API health check is `http://localhost:8000/api/v1/health`; OpenAPI docs are at `http://localhost:8000/docs`.

### Start the web app

```powershell
cd web
Copy-Item .env.example .env
npm install
npm run dev
```

### Run the Flutter app

```powershell
cd mobile
flutter create . --platforms=android
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
```

`10.0.2.2` reaches the host computer from an Android emulator. For a physical device, set `API_BASE_URL` to the computer's LAN IP. The initial `flutter create` generates Android runner files because Flutter is unavailable in this scaffolding environment.

### Create MongoDB indexes

From the repository root:

```powershell
backend\.venv\Scripts\python database/scripts/create_indexes.py
```

No university, student, or scholarship records are seeded by the foundation.

For the Part 2 MongoDB design, see [database/README.md](database/README.md). It documents the 15 collections, initializes their indexes, provides explicitly synthetic demo seed data, and includes a backend-repository CRUD smoke test.

## Status

Project foundation established. Authentication and all product features remain unimplemented.
