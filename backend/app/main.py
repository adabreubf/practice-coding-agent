import logging
import warnings

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.auth import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    SECRET_KEY,
    _DEFAULT_SECRET_KEY,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from app.models import LoginRequest, RefreshRequest, TokenResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if SECRET_KEY == _DEFAULT_SECRET_KEY:
        warnings.warn(
            "Using the default SECRET_KEY. Set the SECRET_KEY environment variable "
            "before deploying to production.",
            stacklevel=1,
        )
        logger.warning(
            "SECURITY WARNING: SECRET_KEY is not set. "
            "Using an insecure default. Do NOT use this in production."
        )
    yield


app = FastAPI(
    lifespan=lifespan,
    title="JWT Auth API",
    description="FastAPI application demonstrating JWT authentication with login and token refresh.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/auth/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    """Authenticate with username/password and receive JWT access and refresh tokens."""
    if not authenticate_user(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": request.username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post("/auth/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh(request: RefreshRequest):
    """Exchange a valid refresh token for a new access token and refresh token."""
    try:
        payload = verify_refresh_token(request.refresh_token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    token_data = {"sub": payload["sub"]}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
