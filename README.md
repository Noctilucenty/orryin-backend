# Orryin Backend — MVP v1

[![FastAPI](https://img.shields.io/badge/FastAPI-0.1.0-009688?logo=fastapi&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-TBD-lightgrey)](#)

Backend MVP that validates Orryin’s **end-to-end flow** for cross-border investing infrastructure:
**Users → KYC (Sumsub) → FX (Wise sandbox) → Brokerage (DriveWealth mock)**.

> **MVP intent:** system validation & integration scaffolding — **not production-ready**.

---

## What this MVP proves

- ✅ User + cash account creation
- ✅ Idempotent Sumsub applicant creation (**handles 409 already-exists**)
- ✅ KYC status fetch endpoint for app UI
- ✅ Wise FX rate fetch + sandbox transfer simulation
- ✅ DriveWealth onboarding (mock) + account persistence
- ✅ One-call **system test** returning a unified JSON snapshot

---

## Tech stack

- **FastAPI**
- **SQLAlchemy 2.0**
- **Pydantic v2**
- **SQLite (dev)** — auto-creates tables on startup
- **httpx** for external calls

---

## Repo structure

```
orryin-backend/
  app/
    main.py                 # FastAPI app + SQLite dev table init
    config.py               # settings (loads env vars)
    db.py                   # SQLAlchemy engine/session/base
    models/                 # ORM tables
    routers/                # API routes
    integrations/           # Sumsub/Wise/DriveWealth clients
  .env                      # local dev (DO NOT commit)
  requirements.txt / pyproject.toml
```

---

## Quickstart (local)

### 1) Create venv + install deps

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2) Configure environment

Create a `.env` file in the repo root (example keys):

```env
DB_URL=sqlite:///./orryin_dev.db
DB_ECHO=false

SUMSUB_BASE_URL=https://api.sumsub.com
SUMSUB_LEVEL_NAME=basic-kyc-level
SUMSUB_APP_TOKEN=your_token
SUMSUB_SECRET_KEY=your_secret

WISE_BASE_URL=https://api.sandbox.transferwise.tech
WISE_API_TOKEN=your_token

DRIVEWEALTH_BASE_URL=https://mock.local
DRIVEWEALTH_API_TOKEN=mock
```

> **Never commit `.env`, database files, or `.venv/`.** Use `.gitignore`.

### 3) Run the server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger UI:
- `http://127.0.0.1:8000/docs`

---

## System test endpoint (one-call validation)

### `POST /mvp/test-flow`

Runs:
1) create dev user & cash account  
2) create/reuse KYC applicant (idempotent)  
3) fetch FX rate + sandbox quote/transfer  
4) create brokerage account (mock)  
5) return unified JSON snapshot

This is the MVP “smoke test” to confirm the backend wiring is intact.

---

## Key KYC endpoints

- `POST /kyc/applicant` — create applicant (**idempotent**, 409-safe)
- `GET /kyc/status?user_id=<id>` — fetch current KYC status (for UI)
- `POST /kyc/webhook/sumsub` — webhook to update approval state

**Idempotent logic**
- If a KYC row exists for `user_id`, return it (no new Sumsub call).
- If Sumsub returns **409 already exists**, treat as success and parse `applicant_id`.

---

## Database notes

- SQLite is used **for dev only**.
- Tables auto-create on startup when `DB_URL` is SQLite.
- For production: migrate to **PostgreSQL** with proper migrations (Alembic).

---

## Troubleshooting

### “409 applicant already exists” in UI
That’s expected — the backend treats it as success and returns `status=already_exists`.

### Uvicorn “Unable to create process … file not found”
Common on Windows when the venv path changed or the venv got recreated.
Fix:
1) `deactivate`
2) re-activate venv
3) run `python -m uvicorn app.main:app --reload` (uses the active python)

---

## Security / compliance reminder

This MVP may reference regulated workflows (KYC/AML) but **does not implement production-grade security**:
- no hardened auth
- no encryption-at-rest strategy
- no audit logs
- no rate limits / abuse protection
- no secrets management

---

## Status

- ✅ Backend MVP v1
- 🟡 Frontend integration in progress
- 🟡 Postgres + migrations (Alembic) pending
- 🟡 Production hardening pending

---

## License

TBD
