# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---------- App ----------
    app_env: str = "dev"
    app_name: str = "Orryin Backend"
    app_debug: bool = True

    # ---------- Database ----------
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "orryin_dev"
    db_user: str = "orryin_user"
    db_password: str = "supersecret_password"
    db_echo: bool = False
    database_url: str | None = None

    @property
    def db_url(self) -> str:
        """
        Returns full DB URL.
        If database_url is not set, fallback to SQLite for dev.
        """
        if self.database_url:
            return self.database_url
        return "sqlite:///./orryin_dev.db"

    # ---------- Sumsub ----------
    sumsub_app_token: str | None = None
    sumsub_secret_key: str | None = None
    sumsub_base_url: str = "https://api.sumsub.com"
    sumsub_level_name: str = "basic-kyc-id-doc"
    sumsub_webhook_secret: str | None = None

    # ---------- Wise (NEW) ----------
    wise_api_key: str | None = None
    wise_base_url: str = "https://api.sandbox.transferwise.tech"
    wise_profile_id: str | None = None


    # ---------- Config ----------
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

        # DriveWealth
    drivewealth_base_url: str = "https://api.drivewealth.io"  # placeholder
    drivewealth_app_key: str | None = None
    drivewealth_app_secret: str | None = None

    # For now we'll use a local mock instead of real HTTP calls
    drivewealth_use_mock: bool = True

# Instantiate global settings instance
settings = Settings()
