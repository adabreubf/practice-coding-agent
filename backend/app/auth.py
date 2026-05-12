import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

_DEFAULT_SECRET_KEY = "supersecretkey_change_in_production"
SECRET_KEY = os.getenv("SECRET_KEY", _DEFAULT_SECRET_KEY)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 86400  # 24 hours

# Hardcoded credentials for demo purposes
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


def authenticate_user(username: str, password: str) -> bool:
    return username == VALID_USERNAME and password == VALID_PASSWORD


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    payload.update({"exp": expire, "type": "access"})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS)
    payload.update({"exp": expire, "type": "refresh"})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def verify_refresh_token(token: str) -> dict:
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise InvalidTokenError("Not a refresh token")
        return payload
    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired refresh token") from exc
