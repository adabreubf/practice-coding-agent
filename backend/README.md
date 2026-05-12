# JWT Auth API

A minimal **FastAPI** Web API that demonstrates JSON Web Token (JWT) authentication.  
It exposes two endpoints: one to obtain a token pair (access + refresh) and one to refresh the tokens.

---

## Table of Contents

- [Features](#features)
- [Endpoints](#endpoints)
- [Requirements](#requirements)
- [Getting Started (Local)](#getting-started-local)
- [Getting Started (Docker)](#getting-started-docker)
- [Configuration](#configuration)
- [Running Tests](#running-tests)

---

## Features

- Login endpoint that validates credentials and returns a signed JWT **access token** (expires in **300 seconds**) plus a **refresh token** (expires in 24 hours).
- Refresh endpoint that accepts a valid refresh token and issues a new token pair.
- Built with **FastAPI** and **PyJWT**.
- Dependencies managed with **Poetry**.
- Fully containerised with **Docker** and **docker-compose**.

---

## Endpoints

| Method | Path           | Description                              |
|--------|----------------|------------------------------------------|
| GET    | `/health`      | Health-check – returns `{"status":"ok"}` |
| POST   | `/auth/login`  | Authenticate and receive JWT tokens      |
| POST   | `/auth/refresh`| Exchange a refresh token for a new pair  |

Interactive API docs are available at [`http://localhost:8000/docs`](http://localhost:8000/docs) once the server is running.

### POST `/auth/login`

**Request body (JSON)**:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200)**:

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Error (401)** — wrong credentials:

```json
{
  "detail": "Invalid username or password"
}
```

### POST `/auth/refresh`

**Request body (JSON)**:

```json
{
  "refresh_token": "<jwt>"
}
```

**Response (200)** — same shape as `/auth/login`.

**Error (401)** — invalid / expired token.

---

## Requirements

- Python ≥ 3.11
- [Poetry](https://python-poetry.org/docs/#installation) ≥ 1.8  
  _or_ Docker + docker-compose

---

## Getting Started (Local)

```bash
# 1. Install dependencies
cd backend
poetry install

# 2. Run the development server
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

**Quick test with curl:**

```bash
# Login
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | python3 -m json.tool

# Refresh (replace <REFRESH_TOKEN> with the value from the login response)
curl -s -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<REFRESH_TOKEN>"}' | python3 -m json.tool
```

---

## Getting Started (Docker)

```bash
cd backend

# Build and start the container
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

To stop:

```bash
docker-compose down
```

---

## Configuration

| Environment variable | Default                            | Description                          |
|----------------------|------------------------------------|--------------------------------------|
| `SECRET_KEY`         | `supersecretkey_change_in_production` | Secret used to sign JWT tokens. **Change this in production.** |

Set the variable in a `.env` file next to `docker-compose.yml` or pass it directly:

```bash
SECRET_KEY=my-super-secret docker-compose up
```

---

## Running Tests

```bash
cd backend
poetry install          # installs dev dependencies too
poetry run pytest -v
```
