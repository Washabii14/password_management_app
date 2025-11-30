## Password Manager Backend — Overview

This repository contains the **backend** for a zero‑knowledge, hardware‑assisted password manager.  
It is designed as a **modular monolith** (FastAPI + Postgres + S3) with strong client‑side cryptography (defined in the Flutter app, in a separate repo) and **per‑entry encrypted sync**.


---

## 1. Project Purpose

- **Zero‑knowledge password manager**:
  - Backend never sees plaintext secrets, Master Password (MPW), Master Key (MK), or VaultKey (VK).
  - It stores only **encrypted blobs and metadata**.
- **Secure key hierarchy** (implemented on the client side):
  - MPW → Argon2id → MK → (encrypts VK) → SQLCipher-encrypted vault.
  - Platform hardware key (HK) wraps MK → WMK stored in secure storage.
- **Cross‑device, offline‑first sync**:
  - Per‑entry encrypted blobs, with versioning and manual conflict resolution.
- **Freemium product**:
  - Backend manages accounts, sessions, plan/feature flags, and (later) subscription billing.

This repo focuses on the **backend**; the Flutter client (Android/iOS/Windows) lives in a separate project.

---

## 2. How This Repo Is Organized

### 2.1 Public Docs (finalized, publication‑ready)

For high‑level sharing and documentation (without open issues or process details), use `public_docs/`:

- `01_Architecture_Overview.md` — concise system architecture summary.
- `02_Key_Management_Model.md` — finalized key hierarchy and flows.
- `03_Design_Pattern_and_Architecture_Style.md` — chosen design patterns and rationale.
- `04_Tech_Stack_Final.md` — finalized tech stack for backend and client.
- `05_Folder_Structure_Final.md` — final backend folder structure.

These files are meant for **contributors, external audiences, documentation sites, or executive summaries**.

### 2.2 Backend Code Layout

Current structure:

```text
app/
  __init__.py
  main.py                 # FastAPI app entrypoint, /health and router include
  api/
    deps.py               # Shared dependencies (DB session, current user, OAuth)
    v1/
      auth_routes.py      # /api/v1/auth routes (register, login, tokens)
  core/
    config.py             # Settings (env-based), DB URL, JWT config
    security.py           # Password hashing, JWT creation/verification
  db/
    base.py               # SQLAlchemy Base
    session.py            # Engine + SessionLocal + get_db()
    models/
      user.py             # User, Device, Session ORM models
  repositories/
    postgres/
      base.py             # BaseRepository wrapper
      auth_repo.py        # User/device/session persistence
  schemas/
    auth_schemas.py       # Pydantic models for auth requests/responses
  services/
    auth_service.py       # Registration, login, token issuing

infra/
  docker/
    Dockerfile.app         # Backend container image definition
    docker-compose.dev.yml # Dev stack: app + Postgres + MinIO

requirements.txt           # Pinned Python dependencies
public_docs/               # Finalized, publication-ready documentation
```

This will grow as Phase 1 features are implemented (vault/sync endpoints, billing, etc.).

---

## 3. Getting Started (Backend Developer)

### 3.1 Option A — Local Python Environment

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate         # macOS / Linux
# .venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Then:
- Health check: `GET http://127.0.0.1:8000/health`
- Auth endpoints (once DB/migrations are wired): `POST /api/v1/auth/register`, `POST /api/v1/auth/login`

You will still need a Postgres instance and (later) S3-compatible storage; for that, Docker is recommended even if you run the app locally.

### 3.2 Option B — Docker Dev Stack (recommended)

1. **Create `.env`** at the repo root (see variables documented in `12_prj_folder_structure.md`), e.g.:

```bash
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=pw_manager
POSTGRES_PASSWORD=pw_manager_password
POSTGRES_DB=pw_manager_dev
DATABASE_URL=postgresql+psycopg://pw_manager:pw_manager_password@db:5432/pw_manager_dev

S3_ENDPOINT_URL=http://s3:9000
S3_ACCESS_KEY_ID=dev-access-key
S3_SECRET_ACCESS_KEY=dev-secret-key
S3_REGION=us-east-1
S3_BUCKET_VAULT_BLOBS=pw-manager-vault-blobs-dev

JWT_SECRET_KEY=CHANGE_ME_IN_DEV
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=info
```

2. **Run the dev stack**:

```bash
cd infra/docker
docker compose -f docker-compose.dev.yml up --build
```

Services:
- API: `http://localhost:8000`
- Health check: `GET /health`
- Postgres: `localhost:5432`
- MinIO console: `http://localhost:9001` (user: `dev-access-key`, password: `dev-secret-key`)

---

## 4. Phase 1 Scope (What’s Being Implemented Now)

Phase 1 backend:

- **Auth & Accounts**:
  - Email + password registration/login.
  - Magic link and OAuth (Google/Apple) after core login is stable.
  - Per-device sessions and refresh tokens.
- **Vault & Sync**:
  - Data model and endpoints for **per-entry encrypted blob** sync.
  - Versioning and manual conflict resolution hooks.
- **Infrastructure**:
  - Local dev stack (app + Postgres + MinIO).
  - Migrations, logging, and basic observability.
- **Pricing**:
  - Plan and feature-flag modeling; real billing integration deferred to a later phase.

The Flutter client (separate repo) will implement the crypto/key-management flows and call these APIs.

---

## 5. How a Newcomer Can Catch Up Quickly

If you’re new to this repo, you can:

1. Read the **public docs** (`public_docs/`) for a high-level understanding:
   - Architecture overview.
   - Key management model.
   - Design pattern and architecture style.
   - Tech stack and folder structure.
2. Explore the `app/` folder:
   - Start with `app/main.py` and `app/api/v1/auth_routes.py`.
   - Then look at `core/`, `db/`, `repositories/`, `schemas/`, and `services/` to see how the layers connect.
3. Run the app locally (see “Getting Started” section) and experiment with the `/health` and auth endpoints as they are implemented.


