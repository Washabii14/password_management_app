from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import Device, Session as SessionModel, User
from app.repositories.postgres.base import BaseRepository


class AuthRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    # User
    def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def create_user(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Device
    def create_or_update_device(
        self, user_id: int, name: str, platform: str
    ) -> Device:
        stmt = select(Device).where(
            Device.user_id == user_id,
            Device.name == name,
            Device.platform == platform,
        )
        device = self.db.execute(stmt).scalar_one_or_none()
        if device is None:
            device = Device(user_id=user_id, name=name, platform=platform)
            self.db.add(device)
        device.last_seen_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(device)
        return device

    # Sessions
    def create_session(
        self,
        user_id: int,
        device_id: int,
        refresh_token_hash: str,
        expires_at: datetime,
    ) -> SessionModel:
        session = SessionModel(
            user_id=user_id,
            device_id=device_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session_by_refresh_hash(
        self, refresh_token_hash: str
    ) -> Optional[SessionModel]:
        stmt = select(SessionModel).where(
            SessionModel.refresh_token_hash == refresh_token_hash
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def revoke_session(self, session: SessionModel) -> None:
        session.revoked_at = datetime.utcnow()
        self.db.commit()


