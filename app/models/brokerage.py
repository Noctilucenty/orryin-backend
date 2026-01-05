# app/models/brokerage.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class BrokerageAccount(Base):
    __tablename__ = "brokerage_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # e.g. "drivewealth"
    broker: Mapped[str] = mapped_column(String(64), default="drivewealth")

    # IDs on broker side
    external_customer_id: Mapped[str] = mapped_column(String(128), index=True)
    external_account_id: Mapped[str] = mapped_column(String(128), index=True)

    status: Mapped[str] = mapped_column(
        String(32), default="created"
    )  # created / active / closed / error

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = relationship("User", backref="brokerage_accounts")
