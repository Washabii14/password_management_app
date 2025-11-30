## Design Pattern & Architecture Style (Final)

This document describes the **final design pattern and architecture style** chosen for the password manager backend and how it relates to the overall system.

---

## 1. Overall Style: Modular Monolith with Clean / Hexagonal Architecture

- The backend is implemented as a **single deployable service** (monolith) that is:
  - **Modular**: code is organized by features (auth, vault/sync, billing, infrastructure).
  - **Hexagonal/Clean**: clear separation between:
    - **Domain**: core business rules and entities.
    - **Application/Services**: use‑case orchestration.
    - **Adapters**: HTTP API, database, and object storage.

### 1.1 Motivation

- **Security and correctness first**:
  - Crypto and key‑management rules are easier to reason about when they are centralized in clear domain and service layers.
- **Maintainability**:
  - Each feature (auth, vault, billing) lives in its own module with well‑defined responsibilities.
- **Future‑proofing**:
  - If needed, individual modules (e.g., vault or billing) can be extracted into separate services later, without redesigning the domain.

---

## 2. Layer Breakdown

### 2.1 Domain Layer

- Contains:
  - Entities and value objects for **users, devices, sessions, vaults, entries, plans**.
  - Interfaces (ports) describing what persistence and external services must provide (e.g., `AuthRepositoryPort`, `VaultRepositoryPort`, `BlobStoragePort`).
- Does **not** depend on FastAPI, SQLAlchemy, or any external framework.

### 2.2 Application / Service Layer

- Implements use cases and orchestrates domain + ports:
  - `AuthService`:
    - Registration, login, password verification.
    - Issuing access tokens and refresh tokens.
    - Creating/updating device and session records.
  - `VaultService` / `SyncService` (future work in Phase 1):
    - Managing entries and per‑entry encrypted blob sync.
    - Detecting version conflicts and exposing them to the client.
  - `BillingService` (later in Phase 1):
    - Managing plan/feature flags and subscription metadata.
- Depends on domain abstractions and repository interfaces.

### 2.3 Adapters Layer

- **HTTP Inbound (FastAPI routers)**:
  - Under `app/api/v1/`:
    - `auth_routes.py` handles HTTP requests, validates input, and delegates to services.
  - Thin endpoints: no business logic, mainly mapping HTTP to service calls.

- **Persistence Outbound (Postgres)**:
  - Under `app/repositories/postgres/`:
    - `auth_repo.py`, `vault_repo.py`, etc.
  - Encapsulate SQLAlchemy logic and map between domain entities and DB models.

- **Storage Outbound (S3 / MinIO)**:
  - Under `app/repositories/storage/` (to be extended):
    - Blob storage adapter for per‑entry encrypted blobs.

---

## 3. Supporting Patterns

Several well‑known patterns support the architecture:

- **Repository Pattern**:
  - Repositories hide persistence details (SQLAlchemy queries, S3 calls).
  - Services depend on interfaces rather than raw DB or HTTP clients.

- **Service / Use‑Case Layer**:
  - Concentrates business rules and workflows in classes like `AuthService` and `VaultService`.
  - Makes it easier to unit test business logic without HTTP or DB.

- **Adapter Pattern**:
  - Separate adapters for:
    - Frameworks (FastAPI routers).
    - External systems (Postgres, S3, secure storage).
  - Allows easier mocking in tests and swapping implementations.

- **State Management (Client, for context)**:
  - The Flutter client uses **Riverpod** to manage application state and compose dependencies, mirroring the backend’s modular structure.

---

## 4. Benefits and Trade‑offs

### Benefits

- **Clarity and security**:
  - Easier threat modeling and code review because sensitive logic (auth, crypto, sync rules) is located in predictable places.
- **Testability**:
  - Domain and service layers can be tested without running a full stack or touching the network.
- **Scalability of complexity**:
  - Features can grow in depth (e.g., shared vaults, billing) without turning the codebase into a “big ball of mud.”

### Trade‑offs

- Slightly more initial structure and boilerplate compared to a simple “routes + models” API.
- Requires discipline:
  - Controllers should stay thin.
  - Domain should not depend on specific DB/HTTP libraries.

Overall, this pattern offers a strong balance of **security**, **maintainability**, and **evolution over time**, which matches the long‑term goals of the password manager project.


