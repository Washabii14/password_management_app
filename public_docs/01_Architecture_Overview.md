## Password Manager — Architecture Overview (Final)

This document summarizes the **final architecture** of the password manager system for publication and high‑level reference.

---

## 1. System Components

- **Client (separate repo)**:
  - Flutter app for **Android, iOS, Windows** (Phase 1).
  - Responsible for **all cryptography and key management**.
  - Stores an encrypted vault locally using **SQLCipher**.
  - Communicates with the backend over HTTPS using encrypted blobs only.

- **Backend (this repo)**:
  - **FastAPI** application.
  - **Postgres** database for users, devices, sessions, vault and entry metadata, and plan/feature flags.
  - **S3‑compatible object storage** (e.g., S3, MinIO) for encrypted vault entry blobs and exports.
  - Manages authentication, per‑device sessions, sync metadata, and freemium plans.

---

## 2. High-Level Data Flow

1. **User and device**
   - User interacts with the Flutter client on a device (mobile or desktop).
   - The client derives a **Master Key (MK)** from the Master Password (MPW) using Argon2id.
   - A random **VaultKey (VK)** encrypts the local SQLCipher database.

2. **Key management (client‑side)**
   - MK is wrapped by a **hardware key (HK)** from Secure Enclave / Android Keystore / OS equivalent, producing a **Wrapped Master Key (WMK)**.
   - WMK is stored in platform secure storage (e.g., Keychain, Keystore).
   - VK is always stored encrypted; MK and VK only exist in memory after unlock.

3. **Sync (per-entry encrypted blobs)**
   - Each vault entry is encrypted on the client.
   - The ciphertext and associated metadata (entry ID, version, timestamps, deleted flags) are synced with the backend.
   - Backend stores:
     - **Metadata** in Postgres.
     - **Ciphertext blobs** in S3.
   - No plaintext secrets or keys are ever sent to or stored on the backend.

4. **Backend responsibilities**
   - **Auth & identity**:
     - Email + password login.
     - Magic link login.
     - OAuth (Google, Apple, etc.).
   - **Sessions & security**:
     - Per‑device sessions with refresh tokens.
     - Access tokens (JWT) for API access.
     - Basic rate limiting and metadata‑only logging.
   - **Vault & sync**:
     - List vaults and entries.
     - Provide change feeds per entry with versioning.
     - Support manual conflict resolution in the client.
   - **Plans & features**:
     - Track plan (free vs paid) and feature flags.
     - Real billing integration is planned for later phases.

---

## 3. Architectural Style

- The backend is implemented as a **modular monolith** using **Clean/Hexagonal Architecture**:
  - **Domain layer**: core business rules and entities (auth, vault, billing).
  - **Application/services layer**: orchestrates domain operations and coordinates repositories.
  - **Adapters**:
    - FastAPI routers (HTTP in).
    - Postgres repositories and S3 clients (I/O out).
  - This structure retains a single deployable backend service while keeping clear boundaries for future growth.

---

## 4. Security Principles

- **Zero‑knowledge**:
  - Backend never has access to MPW, MK, VK, WMK, or decrypted entries.
  - Only ciphertext and metadata are stored server‑side.

- **Hardware‑assisted key protection** (client):
  - Hardware key (HK) is used to wrap MK (WMK).
  - Biometric unlock gated by the platform, not by the backend.

- **Defense in depth**:
  - Strong KDF (Argon2id) and AES‑GCM encryption.
  - Per‑device sessions, short‑lived access tokens with refresh tokens.
  - Metadata‑only logging and GDPR‑friendly data handling.


