from datetime import datetime, timedelta, timezone
import os
from uuid import uuid4

import jwt
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 3600
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-key-change-me-123456",
)
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

app = FastAPI(title="JWT Web API", version="0.1.0")


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_SECONDS


def _create_token(subject: str, token_type: str, expires_in: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "jti": str(uuid4()),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def _build_token_response(username: str) -> TokenResponse:
    return TokenResponse(
        access_token=_create_token(username, "access", ACCESS_TOKEN_EXPIRE_SECONDS),
        refresh_token=_create_token(username, "refresh", REFRESH_TOKEN_EXPIRE_SECONDS),
    )


@app.post("/auth/token", response_model=TokenResponse)
def create_token(credentials: LoginRequest) -> TokenResponse:
    if (
        credentials.username != VALID_USERNAME
        or credentials.password != VALID_PASSWORD
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return _build_token_response(credentials.username)


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest) -> TokenResponse:
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from exc

    if decoded.get("type") != "refresh" or not decoded.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return _build_token_response(decoded["sub"])
