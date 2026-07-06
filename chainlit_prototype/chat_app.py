"""
챗봇 백엔드 로직(SafetyService → Retriever → OpenAI 스트리밍)을 화면 없이 빠르게
눈으로 확인하기 위한 임시 프로토타입이다.

⚠ 실제 제품이 아니다 — 정식 화면은 frontend/src/pages/ChatPage/ChatPage.tsx.
DB 저장 없이 app/services/의 실제 로직만 재사용하며(로그인/세션/기록 저장 생략),
RAG가 아직 stub이라 Retriever는 항상 빈 결과를 준다 (app/services/retriever.py 참고).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import chainlit as cl

from app.services import safety_service
from app.services.llm_client import stream_reply
from app.services.retriever import Retriever

retriever = Retriever()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    text = message.content

    if safety_service.contains_emergency_keyword(text):
        await cl.Message(content=safety_service.EMERGENCY_FALLBACK_MESSAGE).send()
        return

    context: dict = {"conditions": [], "medications": [], "goals": []}
    chunks = retriever.search(text, context)

    reply = cl.Message(content="")
    await reply.send()
    async for token in stream_reply(text, context, chunks):
        await reply.stream_token(token)
    await reply.update()
