## Key Management Model (Final)

This document summarizes the **final key management model** used by the password manager.  
All cryptographic operations and key handling are performed **on the client**; the backend remains zero‑knowledge.

---

## 1. Key Types

- **Master Password (MPW)**  
  User‑chosen password, never stored or sent to the backend.

- **Master Key (MK)**  
  256‑bit symmetric key derived from MPW:
  \[
  \text{MK} = \text{Argon2id}(\text{MPW}, \text{salt}, \text{params})
  \]

- **VaultKey (VK)**  
  Random 256‑bit symmetric key used to encrypt the vault data (SQLCipher database).

- **Hardware Key (HK)**  
  Hardware‑backed key generated and stored in:
  - iOS Secure Enclave.
  - Android Keystore / StrongBox.
  - OS‑equivalent mechanism on other platforms where available.

- **Wrapped Master Key (WMK)**  
  MK encrypted with HK (e.g., AES‑KWP or RSA‑OAEP, depending on platform):
  \[
  \text{WMK} = \text{Enc}_{\text{HK}}(\text{MK})
  \]
  WMK is stored in the platform’s secure storage (Keychain/Keystore).

---

## 2. Setup Flow (First Run)

1. User creates a **Master Password (MPW)**.
2. Client generates a random **salt** and **KDF parameters** (Argon2id: memory, iterations, parallelism).
3. Derive **MK** from MPW, salt, and params.
4. Generate a random **VaultKey (VK)**.
5. Encrypt the local vault (SQLCipher DB) using VK.
6. Request/generate **HK** via the platform’s secure element.
7. Wrap MK with HK → **WMK**; store WMK in secure storage.
8. Store KDF metadata (salt, params, KDF type) locally and, as non‑secret but sensitive metadata, on the backend for easier migration.

---

## 3. Unlock Flows

### 3.1 Unlock with Biometrics

1. User authenticates via biometrics (Face ID, Touch ID, fingerprint, etc.).
2. Platform allows HK operations.
3. Client decrypts WMK using HK to recover **MK** in memory.
4. Client decrypts **VK** (which is stored encrypted with MK).
5. Client mounts the SQLCipher DB with VK and decrypts entries on demand.

### 3.2 Unlock with Master Password (Fallback)

1. User enters **MPW**.
2. Client loads KDF metadata (salt + params) from local storage.
3. Derives **MK** using Argon2id.
4. Decrypts **VK** with MK.
5. Mounts SQLCipher DB with VK and decrypts entries as needed.

---

## 4. Key Rotation (Change Master Password)

1. User provides old MPW; derive old MK.
2. Decrypt VK using old MK.
3. User chooses new MPW; derive new MK' using new salt and KDF params.
4. Re‑encrypt VK with MK' (vault content encrypted with VK does **not** need to be re‑encrypted).
5. Wrap MK' with HK → new WMK; store updated WMK in secure storage.
6. Update local and backend KDF metadata (salt, params, version).

---

## 5. Device Migration

- **Export**:
  - Client generates an export bundle containing:
    - Encrypted vault database.
    - KDF metadata: KDF type, salt, params, version.
    - Non‑sensitive vault metadata.
  - Bundle does **not** contain MK, VK, or WMK.

- **Import on a new device**:
  - User imports the bundle and enters MPW.
  - Client derives MK from MPW and KDF metadata.
  - VK is decrypted, vault is mounted, and new HK/WMK are created for the new device.
  - Biometrics must be re‑enrolled on the new device.

---

## 6. Security Properties

- **Zero‑knowledge backend**:
  - Backend never receives MPW, MK, VK, WMK, or plaintext entries.
  - Only ciphertext, KDF metadata, and sync metadata (IDs, versions, timestamps) are stored server‑side.

- **Hardware‑assisted protection**:
  - MK is protected by HK when at rest (via WMK).
  - Biometric policies are enforced by the platform, not the backend.

- **Resilience against backend compromise**:
  - An attacker with full backend access gets:
    - Encrypted blobs.
    - KDF salts and parameters.
  - Without MPW, offline brute‑force is the main risk, mitigated by:
    - Strong MPW policy.
    - Argon2id with conservative parameters tuned per device.


