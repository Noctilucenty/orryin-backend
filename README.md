# Orryin Backend — MVP v1

## Overview

Orryin is a backend system designed to enable **global (non‑U.S.) users** to access U.S. investing infrastructure in a compliant, modular way.

This repository contains the **Backend MVP v1**, focused on validating:
- User creation
- KYC onboarding (Sumsub)
- FX payments (Wise – sandbox)
- Brokerage account creation (DriveWealth – mock)
- End‑to‑end system orchestration

This MVP is **system‑validation focused**, not production‑ready.

---

## Tech Stack

- **FastAPI** – API framework  
- **SQLAlchemy (2.0)** – ORM  
- **SQLite (dev)** – Local development DB  
- **Pydantic v2** – Data validation  
- **httpx** – External API calls  

---

## Architecture

```
Client (Web / Mobile)
        ↓
FastAPI Backend
        ↓
------------------------------------------------
| Users | KYC | Payments | Brokerage | MVP Flow |
------------------------------------------------
        ↓
 External Services (Sandbox / Mock)
   - Sumsub (KYC)
   - Wise (FX)
   - DriveWealth (Brokerage)
```

---

## Key Endpoint — System Test

### POST `/mvp/test-flow`

Runs the full backend MVP flow:

1. Create dev user & cash account  
2. Create or reuse KYC applicant (idempotent)  
3. Fetch FX rate and simulate transfer  
4. Create brokerage account (mock)  
5. Return a unified JSON snapshot  

This endpoint is used to validate **system integrity end‑to‑end**.

---

## KYC

```
POST /kyc/applicant
GET  /kyc/status
POST /kyc/webhook/sumsub
```

- Idempotent applicant creation
- Handles Sumsub `409 already exists`
- Webhook updates approval status

---

## Payments

```
GET  /payments/fx-rate
POST /payments/transfer/sandbox
```

---

## Brokerage

```
POST /brokerage/onboard
GET  /brokerage/accounts/{user_id}
```

---

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## Database

- SQLite is used **only for development**
- Tables auto‑create on startup
- Designed for PostgreSQL migration

---

## Status

✅ Backend MVP v1 complete  
🟡 Frontend pending  
🟡 Production hardening pending  

---

## Disclaimer

This repository is a **technical MVP**, not production software.
It exists to validate architecture, integrations, and system flows.
