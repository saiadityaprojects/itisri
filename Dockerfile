FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY itisri/ ./itisri/
COPY demo_agent/ ./demo_agent/
COPY benchmark/ ./benchmark/
COPY tests/ ./tests/

RUN pip install --upgrade pip && pip install -e ".[dev]"

CMD ["python", "-m", "demo_agent.run"]
