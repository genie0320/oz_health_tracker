FROM python:3.12-slim

WORKDIR /code

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /code/
RUN uv sync --group ai --no-dev --no-install-project

COPY ai_worker /code/ai_worker

CMD ["uv", "run", "uvicorn", "ai_worker.sync_api:app", "--host", "0.0.0.0", "--port", "8100"]
