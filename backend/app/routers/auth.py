from datetime import UTC, datetime
from typing import Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pymongo.errors import DuplicateKeyError
from pymongo.asynchronous.database import AsyncDatabase

from app.core.dependencies import get_current_user
from app.core.security import decode_access_token
from app.db.mongodb import get_database
from app.schemas.auth import CurrentUserResponse, LoginRequest, LogoutResponse, StudentRegistrationRequest, TokenResponse
from app.services.auth import authenticate, register_student, token_response

router = APIRouter(prefix="/auth", tags=["authentication"])
bearer_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def user_response(user: dict[str, Any]) -> CurrentUserResponse:
    return CurrentUserResponse(id=str(user["_id"]), email=user["email"], display_name=user["display_name"], role=user["role"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, summary="Register a student account")
async def register(payload: StudentRegistrationRequest, database: AsyncDatabase = Depends(get_database)) -> TokenResponse:
    try:
        user = await register_student(database, payload.model_dump())
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account or student number already exists") from None
    return TokenResponse(**token_response(user))


@router.post("/login", response_model=TokenResponse, summary="Log in with an approved account")
async def login(payload: LoginRequest, database: AsyncDatabase = Depends(get_database)) -> TokenResponse:
    user = await authenticate(database, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(**token_response(user))


@router.get("/me", response_model=CurrentUserResponse)
async def current_user(current: dict[str, Any] = Depends(get_current_user)) -> CurrentUserResponse:
    return user_response(current)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    token: str = Depends(bearer_scheme), current: dict[str, Any] = Depends(get_current_user), database: AsyncDatabase = Depends(get_database)
) -> LogoutResponse:
    try:
        payload = decode_access_token(token)
        token_id, expires_at = payload.get("jti"), payload.get("exp")
        if not isinstance(token_id, str) or not isinstance(expires_at, (int, float)):
            raise ValueError("Missing token claims")
        expiry = datetime.fromtimestamp(expires_at, UTC)
    except (jwt.PyJWTError, ValueError, OSError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token") from None
    await database["revoked_tokens"].update_one(
        {"jti": token_id}, {"$setOnInsert": {"jti": token_id, "user_id": current["_id"], "expires_at": expiry}}, upsert=True
    )
    return LogoutResponse(status="logged_out", revoked_until=expiry)
