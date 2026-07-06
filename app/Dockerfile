# 템플릿(AI_HealthCare_Final_Project_Template) 방식 참고 — uv로 의존성 관리
FROM python:3.12-slim

WORKDIR /code

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /code/
RUN uv sync --group app --no-dev --no-install-project

COPY app /code/app

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
