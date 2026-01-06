import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine

# Routers
from app.routers.users import router as users_router
from app.routers.kyc import router as kyc_router
from app.routers.payments import router as payments_router
from app.routers.brokerage import router as brokerage_router
from app.routers.mvp import router as mvp_router


def create_app() -> FastAPI:
    app = FastAPI(title="Orryin Backend", version="0.1.0")

    # ---- CORS (IMPORTANT FOR WEB: localhost:8081) ----
    # For MVP, we allow:
    # - Expo web dev server (localhost)
    # - Any Railway app domain
    #
    # NOTE: allow_credentials must be False if we use regex/"*"-style origins.
    cors_allow_origins = [
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:19006",
        "http://127.0.0.1:19006",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_allow_origins,
        allow_origin_regex=r"https://.*\.railway\.app",
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=86400,
    )

    # ---- DB init (MVP: auto-create tables) ----
    # MVP approach: create tables on startup so fresh Postgres works without Alembic.
    @app.on_event("startup")
    def _startup() -> None:
        Base.metadata.create_all(bind=engine)

    # ---- Routes ----
    @app.get("/")
    def health():
        return {"status": "ok", "name": "Orryin Backend", "env": settings.app_env}

    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(kyc_router, prefix="/kyc", tags=["kyc"])
    app.include_router(payments_router, prefix="/payments", tags=["payments"])
    app.include_router(brokerage_router, prefix="/brokerage", tags=["brokerage"])
    app.include_router(mvp_router, prefix="/mvp", tags=["mvp"])

    return app


app = create_app()
