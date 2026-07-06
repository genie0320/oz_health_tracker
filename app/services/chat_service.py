"""
Service 레이어 규칙: 판단은 여기서만 한다. Router는 이 클래스의 메서드만 호출한다.
T-LLM-2 흐름(`docs/sample_code_chat/chat_flow_sequence.mermaid`와 동일):
SafetyService(응급 감지) → UserHealthContextService(컨텍스트) → Retriever(RAG stub)
→ LLM 스트리밍(OpenAI) → ChatRepository(대화 저장).

Retriever/LLM/HealthContext는 생성자로 주입 가능 — 테스트에서 Fake로 교체하기 위함
(CODING_RULES.md §4: 외부 의존성은 항상 Fake로 대체).
"""

import json
from collections.abc import AsyncIterator, Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatSession
from app.repositories.chat_repository import ChatRepository
from app.services import safety_service
from app.services.llm_client import stream_reply
from app.services.retriever import Retriever
from app.services.user_health_context_service import get_user_health_context


class ChatService:
    def __init__(
        self,
        repository: ChatRepository,
        retriever: Retriever | None = None,
        llm_stream: Callable[[str, dict, list[str]], AsyncIterator[str]] | None = None,
        health_context: Callable[[AsyncSession, int], Awaitable[dict]] | None = None,
    ) -> None:
        self.repository = repository
        self._retriever = retriever or Retriever()
        self._llm_stream = llm_stream or stream_reply
        self._health_context = health_context or get_user_health_context

    async def create_session(self, profile_id: int) -> str:
        session = await self.repository.create_session(profile_id)
        return session.session_uuid

    async def get_authorized_session(self, session_uuid: str, profile_id: int) -> ChatSession | None:
        session = await self.repository.get_session_by_uuid(session_uuid)
        if session is None or session.profile_id != profile_id:
            return None
        return session

    async def get_history(self, session_id: int) -> list[dict]:
        messages = await self.repository.history_for(session_id)
        return [{"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()} for m in messages]

    async def stream_message(self, session_id: int, profile_id: int, message: str) -> AsyncIterator[str]:
        """
        응급 키워드가 감지되면 LLM을 호출하지 않고 고정 안내만 반환한다(T-LLM-1 원칙).
        이 경우 대화 기록도 저장하지 않는다 — chat_flow_sequence.mermaid의 분기와 동일.
        """
        if safety_service.contains_emergency_keyword(message):
            chunk = safety_service.with_disclaimer(
                {"type": "emergency_fallback", "content": safety_service.EMERGENCY_FALLBACK_MESSAGE}
            )
            yield json.dumps(chunk, ensure_ascii=False) + "\n"
            return

        context = await self._health_context(self.repository.db, profile_id)
        chunks = self._retriever.search(message, context)

        full_response = ""
        async for token in self._llm_stream(message, context, chunks):
            full_response += token
            yield json.dumps({"type": "token", "content": token}, ensure_ascii=False) + "\n"

        await self.repository.save_message(session_id, profile_id, "user", message)
        await self.repository.save_message(session_id, profile_id, "assistant", full_response)

        done_chunk = safety_service.with_disclaimer({"type": "done", "content": ""})
        yield json.dumps(done_chunk, ensure_ascii=False) + "\n"
