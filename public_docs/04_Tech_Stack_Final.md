## Tech Stack (Final)

This document summarizes the **final chosen technologies** for the password manager system.

---

## 1. Backend

- **Language & Runtime**
  - **Python 3.11** (or compatible 3.x).

- **Web Framework**
  - **FastAPI**
    - Async‑first, high performance.
    - Pydantic‑based request/response models.
    - Easy OpenAPI generation for client integration.

- **Database**
  - **Postgres**
    - Primary relational database.
    - Stores:
      - Users, devices, sessions.
      - Vault and entry metadata (IDs, versions, timestamps, deleted flags).
      - KDF metadata (salt, params) and configuration.
      - Plan/feature‑flag data (free vs paid tiers).

- **Object Storage**
  - **S3‑compatible storage** (AWS S3 in production, MinIO in development).
    - Stores per‑entry **encrypted blobs** and vault export bundles.
    - No plaintext secrets or keys.

- **ORM & Migrations**
  - **SQLAlchemy** for ORM mapping.
  - **Alembic** for schema migrations.

- **Security & Auth**
  - **Passlib** for password hashing on the server side (for server login password, not MPW).
  - **JWT** via `python-jose` (or similar) for:
    - Short‑lived access tokens.
    - Refresh tokens tied to device sessions.
  - OAuth and magic link support via FastAPI routes and provider SDKs (to be integrated).

- **HTTP & Utilities**
  - **HTTPX** for any outgoing HTTP calls (if needed).
  - **orjson** or equivalent for performant JSON serialization (optional).

- **Containerization & Dev Environment**
  - **Docker**, with:
    - `Dockerfile` for the FastAPI app.
    - `docker-compose` for local development stack (app + Postgres + MinIO).

- **Testing**
  - **pytest**, `pytest-asyncio` for async testing.

---

## 2. Client (Flutter) — Context

Although implemented in a separate repository, the backend design assumes the following client stack:

- **Framework**
  - **Flutter**.

- **Platforms (Phase 1)**
  - Android.
  - iOS.
  - Windows.

- **State Management**
  - **Riverpod**.

- **Local Storage**
  - **SQLCipher** (via a Flutter plugin such as `sqflite_sqlcipher` or equivalent) for encrypting the entire local vault database.

- **Crypto & Secure Storage**
  - **Argon2id** for KDF (via a Dart/Flutter package).
  - **AES‑256‑GCM** for encryption/decryption of entries and VK.
  - **flutter_secure_storage** (or equivalent) for storing WMK and other small sensitive values.
  - **local_auth** for biometric unlock integration.

---

## 3. Infrastructure & Operations

- **Local Development**
  - Docker Compose:
    - `app`: FastAPI backend.
    - `db`: Postgres 16.
    - `s3`: MinIO (S3 emulator).

- **Production (planned)**
  - Container‑based deployment (e.g., Kubernetes, ECS, or equivalent).
  - Managed Postgres.
  - Managed S3 or compatible object storage.
  - Centralized logging and metrics (metadata‑only).

---

## 4. Security & Compliance Considerations

- **Zero‑knowledge**: cryptographic ops and key handling occur exclusively on the client.
- **GDPR‑friendly** design:
  - Data minimization.
  - Right‑to‑delete and export considerations.
  - Metadata‑only logging with retention controls.
- **Future compliance targets** (not Phase 1 scope):
  - SOC2 / ISO27001‑style controls and processes.


