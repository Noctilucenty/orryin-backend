# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app import models  # IMPORTANT: registers all ORM models (tables)

from app.routers.users import router as users_router
from app.routers.kyc import router as kyc_router
from app.routers.payments import router as payments_router
from app.routers.brokerage import router as brokerage_router
from app.routers.mvp import router as mvp_router

app = FastAPI(title="Orryin Backend", version="0.1.0")


def _init_db() -> None:
    """
    Create tables if they don't exist.
    For MVP deployments (including Railway Postgres), we rely on SQLAlchemy create_all.
    Safe to call multiple times.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[DB INIT] Failed to create tables: {e}")


@app.on_event("startup")
def on_startup() -> None:
    # MVP: ensure tables exist for both SQLite dev and Postgres deploys
    _init_db()


# MVP CORS: allow all origins to avoid web demo issues.
# Tighten this for production hardening.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(kyc_router, prefix="/kyc", tags=["kyc"])
app.include_router(payments_router, prefix="/payments", tags=["payments"])
app.include_router(brokerage_router, prefix="/brokerage", tags=["brokerage"])
app.include_router(mvp_router, prefix="/mvp", tags=["mvp"])


@app.get("/")
def root():
    return {"status": "ok", "name": settings.app_name, "env": settings.app_env}
