# Build the frontend
FROM node:latest as build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Setup and run the backend
FROM python:3.11-slim
WORKDIR /app


# Install system dependencies including build tools and libc6-dev for static libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    gcc \
    build-essential \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=/app
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Install backend dependencies
COPY ./backend/pyproject.toml ./backend/poetry.lock* /app/backend/
WORKDIR /app/backend
RUN poetry install --no-dev --no-interaction --no-ansi

# Install compiler dependencies and run tests
COPY compiler/ /app/compiler/
WORKDIR /app/compiler
RUN poetry install --no-interaction --no-ansi
RUN poetry run pytest

# Setup container folder structure
COPY backend/ /app/backend/
COPY --from=build-stage /app/frontend/dist /app/backend/static

ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# Run the backend
WORKDIR /app/backend
CMD ["flask", "run", "--no-debugger", "--no-reload"]