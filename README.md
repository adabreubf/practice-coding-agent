# practice-coding-agent

Este repositorio incluye una aplicación Web API en `backend/` construida con **Python**, **FastAPI** y **Poetry** para demostrar un caso de uso de autenticación con **JWT**.

## Estructura

```text
.
├── backend/
│   ├── backend_jwt_api/
│   ├── tests/
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
└── docker-compose.yml
```

## Endpoints

### `POST /auth/token`

Genera un `access_token` con expiración de **300 segundos** y un `refresh_token`.

**Body**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

### `POST /auth/refresh`

Genera un nuevo par de tokens a partir de un `refresh_token` válido.

**Body**

```json
{
  "refresh_token": "TOKEN_AQUI"
}
```

## Uso local con Poetry

```bash
cd backend
poetry install
poetry run uvicorn backend_jwt_api.main:app --host 0.0.0.0 --port 8000
```

La documentación interactiva queda disponible en:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Ejemplos de uso

Obtener token:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Refrescar token:

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"TOKEN_AQUI"}'
```

## Docker

Construir y levantar el servicio:

```bash
docker compose up --build
```

El servicio quedará expuesto en `http://localhost:8000`.

> Puedes sobrescribir `JWT_SECRET_KEY`, `JWT_ADMIN_USERNAME` y `JWT_ADMIN_PASSWORD` en el entorno local o en Docker para personalizar la configuración.
