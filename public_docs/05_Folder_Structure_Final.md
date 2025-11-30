## Project Folder Structure (Final)

This document describes the **final backend folder structure** intended for publication.  
It focuses on how the codebase is organized conceptually, independent of internal discussions or implementation steps.

---

## 1. Top-Level Layout

```text
pw_mngt_backend/
├─ app/                    # Backend application (FastAPI)
├─ infra/                  # Infrastructure & deployment configuration
├─ public_docs/            # Published, finalized documentation (this folder)
├─ requirements.txt        # Python dependencies
└─ README.md               # Project overview & onboarding guide
```

---

## 2. Application (`app/`) Structure

```text
app/
├─ main.py                 # FastAPI app factory, router registration, /health
├─ api/
│  ├─ deps.py              # Shared dependencies (DB session, current user, OAuth)
│  └─ v1/                  # Versioned HTTP API (public surface)
│     └─ auth_routes.py    # Auth endpoints (register, login, tokens, later magic/OAuth)
├─ core/
│  ├─ config.py            # Settings via Pydantic (env-based config, DB URL, JWT)
│  └─ security.py          # Password hashing, JWT handling, core security helpers
├─ db/
│  ├─ base.py              # SQLAlchemy Base class
│  ├─ session.py           # Engine, SessionLocal, dependency to get DB session
│  └─ models/
│     └─ user.py           # ORM models: User, Device, Session
├─ repositories/
│  └─ postgres/
│     ├─ base.py           # BaseRepository wrapper around SQLAlchemy session
│     └─ auth_repo.py      # Auth-related persistence (users, devices, sessions)
├─ schemas/
│  └─ auth_schemas.py      # Pydantic schemas for auth requests/responses
└─ services/
   └─ auth_service.py      # Application logic for auth (register, login, tokens)
```

This structure will be extended with:
- `vault` and `sync` modules (routes, services, repos, schemas).
- `billing` modules for plans and subscriptions.

All features follow the same pattern:
- **API routers** (HTTP layer).
- **Services** (use‑cases).
- **Repositories** (DB/S3 adapters).
- **Schemas** (input/output models).

---

## 3. Infrastructure (`infra/`) Structure

```text
infra/
└─ docker/
   ├─ Dockerfile.app           # Docker image for the FastAPI app
   └─ docker-compose.dev.yml   # Dev stack: app + Postgres + MinIO
```

These files define how to run the backend and its dependencies in containers for development and, with extensions, staging/production.

---

## 4. Documentation Folders

- `public_docs/`
  - **Finalized, publication‑ready documentation**:
    - `01_Architecture_Overview.md`
    - `02_Key_Management_Model.md`
    - `03_Design_Pattern_and_Architecture_Style.md`
    - `04_Tech_Stack_Final.md`
    - `05_Folder_Structure_Final.md` (this file)


