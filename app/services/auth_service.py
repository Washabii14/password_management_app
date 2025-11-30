from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.models.user import User
from app.repositories.postgres.auth_repo import AuthRepository


settings = get_settings()


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = AuthRepository(db)

    # User registration
    def register_user(self, email: str, password: str) -> User:
        existing = self.repo.get_user_by_email(email)
        if existing:
            raise ValueError("User with this email already exists")
        password_hash = hash_password(password)
        return self.repo.create_user(email=email, password_hash=password_hash)

    # Login
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.repo.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def issue_tokens_for_user(
        self, user: User, device_name: str, platform: str
    ) -> Tuple[str, str]:
        # Create / update device
        device = self.repo.create_or_update_device(
            user_id=user.id,
            name=device_name,
            platform=platform,
        )

        # Create access token
        access_token = create_access_token(subject=str(user.id))

        # Create refresh token (reuse access token payload but longer expiry)
        refresh_expires = datetime.utcnow() + timedelta(
            days=30
        )  # example long-lived refresh
        refresh_token = create_access_token(
            subject=str(user.id),
            expires_delta=refresh_expires - datetime.utcnow(),
        )

        # Store hashed refresh token in DB
        refresh_token_hash = hash_password(refresh_token)
        self.repo.create_session(
            user_id=user.id,
            device_id=device.id,
            refresh_token_hash=refresh_token_hash,
            expires_at=refresh_expires,
        )

        return access_token, refresh_token


