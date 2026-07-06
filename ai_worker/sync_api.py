"""
챗봇(T-LLM-2)처럼 즉시 응답이 필요한 요청 전용 — 작은 FastAPI 앱.
메인 백엔드(app/services/chat_service.py)가 이 서비스에 직접 요청한다.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ReMedi AI Worker — Sync API")


class RetrieveRequest(BaseModel):
    query: str
    profile_id: int


class RetrieveResult(BaseModel):
    chunks: list[str]


@app.post("/retrieve", response_model=RetrieveResult)
async def retrieve(req: RetrieveRequest):
    # TODO: 쿼리 임베딩 -> ChromaDB Server Mode 검색 -> 관련 청크 리턴
    return RetrieveResult(chunks=[])


@app.get("/health")
async def health():
    return {"status": "ok"}
