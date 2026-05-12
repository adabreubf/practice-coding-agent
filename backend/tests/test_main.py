from datetime import datetime, timezone

import jwt
from fastapi.testclient import TestClient

from backend_jwt_api.main import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    ALGORITHM,
    JWT_SECRET_KEY,
    app,
)


client = TestClient(app)


def test_create_token_returns_access_token_with_expected_expiration():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    body = response.json()
    decoded = jwt.decode(
        body["access_token"],
        JWT_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    expires_in = decoded["exp"] - decoded["iat"]

    assert body["token_type"] == "bearer"
    assert body["expires_in"] == ACCESS_TOKEN_EXPIRE_SECONDS
    assert expires_in == ACCESS_TOKEN_EXPIRE_SECONDS
    assert decoded["sub"] == "admin"
    assert decoded["type"] == "access"


def test_create_token_rejects_invalid_credentials():
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_refresh_token_returns_new_access_token():
    login_response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )
    original_access_token = login_response.json()["access_token"]

    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": login_response.json()["refresh_token"]},
    )

    assert refresh_response.status_code == 200
    body = refresh_response.json()
    assert body["access_token"] != original_access_token
    decoded = jwt.decode(
        body["access_token"],
        JWT_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert decoded["type"] == "access"
    assert decoded["sub"] == "admin"
    assert decoded["exp"] > int(datetime.now(timezone.utc).timestamp())


def test_refresh_token_rejects_access_token():
    login_response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "admin123"},
    )

    refresh_response = client.post(
        "/auth/refresh",
        json={"refresh_token": login_response.json()["access_token"]},
    )

    assert refresh_response.status_code == 401
    assert refresh_response.json() == {"detail": "Invalid refresh token"}
