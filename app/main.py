"""
FastAPI 진입점. 레이어 우선 구조(apis/services/repositories/models/dtos)로
템플릿(AI_HealthCare_Final_Project_Template)의 폴더 배치를 따른다.
(2026-07 재결정: 도메인 우선 -> 레이어 우선. 이유는 decision_log.md 참고)
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base

from app.apis.v1 import auth_routers, medication_routers, chat_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="ReMedi API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_V1 = "/api/v1"

app.include_router(auth_routers.router, prefix=f"{API_V1}/auth", tags=["Auth"])
app.include_router(medication_routers.router, prefix=f"{API_V1}/medications", tags=["Medications"])
app.include_router(chat_routers.router, prefix=f"{API_V1}/chat", tags=["Chat"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
