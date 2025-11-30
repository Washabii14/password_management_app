from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(255), unique=True, index=True, nullable=False)
    password_hash: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)

    created_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


class Device(Base):
    __tablename__ = "devices"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, index=True, nullable=False)
    name: str = Column(String(255), nullable=False)
    platform: str = Column(String(50), nullable=False)

    last_seen_at: Optional[datetime] = Column(DateTime(timezone=True), nullable=True)


class Session(Base):
    __tablename__ = "sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, index=True, nullable=False)
    device_id: int = Column(Integer, index=True, nullable=False)
    refresh_token_hash: str = Column(String(255), nullable=False)

    expires_at: datetime = Column(DateTime(timezone=True), nullable=False)
    revoked_at: Optional[datetime] = Column(DateTime(timezone=True), nullable=True)


