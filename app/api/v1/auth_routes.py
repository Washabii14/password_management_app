from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep
from app.schemas.auth_schemas import (
    LoginRequest,
    TokenPair,
    UserCreate,
    UserRead,
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db_dep)) -> AuthService:
    return AuthService(db)


@router.post("/register", response_model=UserRead)
def register_user(
    body: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = auth_service.register_user(email=body.email, password=body.password)
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/login", response_model=TokenPair)
def login(
    body: LoginRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.authenticate_user(email=body.email, password=body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Derive a simple device name / platform from request headers for now
    user_agent = request.headers.get("user-agent", "unknown")
    device_name = user_agent[:255]
    platform = "unknown"

    access_token, refresh_token = auth_service.issue_tokens_for_user(
        user=user,
        device_name=device_name,
        platform=platform,
    )
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


