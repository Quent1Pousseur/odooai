# OdooAI Backend — Production Dockerfile
FROM python:3.13-slim AS base

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[prod]" 2>/dev/null || pip install --no-cache-dir .

# App code
COPY odooai/ odooai/

# Non-root user
RUN useradd -m odooai
USER odooai

EXPOSE 8000

CMD ["uvicorn", "odooai.main:app", "--host", "0.0.0.0", "--port", "8000"]
