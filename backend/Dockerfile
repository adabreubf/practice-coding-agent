FROM python:3.12-slim

ENV POETRY_VERSION=2.4.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY backend_jwt_api ./backend_jwt_api

EXPOSE 8000

CMD ["uvicorn", "backend_jwt_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
