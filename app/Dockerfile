# 템플릿(AI_HealthCare_Final_Project_Template) 방식 참고 — uv로 의존성 관리
FROM python:3.12-slim

WORKDIR /code

# asyncmy(MySQL 드라이버)는 사전 빌드된 wheel이 없는 플랫폼(예: arm64)에서 소스 빌드가
# 필요하다 — gcc/MySQL client 헤더가 없으면 uv sync에서 빌드 실패한다.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /code/
RUN uv sync --group app --no-dev --no-install-project

COPY app /code/app

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
