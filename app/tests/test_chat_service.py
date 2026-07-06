"""
가짜(Fake) 의존성으로 격리한 단위테스트 (docs/sample_code_chat/test_chat_service.py와 같은 패턴).
외부 의존성(Repository/Retriever/LLM/HealthContext)은 전부 Fake로 대체해 결정적으로 통과한다
(CODING_RULES.md §4 — 실제 DB/OpenAI 호출 없음).
"""

from dataclasses import dataclass

import pytest

from app.services.chat_service import ChatService
from app.services.safety_service import DISCLAIMER_TEXT, EMERGENCY_FALLBACK_MESSAGE


@dataclass
class FakeSession:
    id: int
    session_uuid: str
    profile_id: int


class FakeChatRepository:
    def __init__(self, sessions: list[FakeSession] | None = None) -> None:
        self.db = None
        self._sessions = {s.session_uuid: s for s in (sessions or [])}
        self.saved_calls: list[tuple[int, int, str, str]] = []

    async def create_session(self, profile_id: int) -> FakeSession:
        session = FakeSession(id=len(self._sessions) + 1, session_uuid=f"uuid-{profile_id}", profile_id=profile_id)
        self._sessions[session.session_uuid] = session
        return session

    async def get_session_by_uuid(self, session_uuid: str) -> FakeSession | None:
        return self._sessions.get(session_uuid)

    async def save_message(self, session_id: int, profile_id: int, role: str, content: str) -> None:
        self.saved_calls.append((session_id, profile_id, role, content))

    async def history_for(self, session_id: int) -> list:
        return []


async def _fake_health_context(db, profile_id: int) -> dict:
    return {"conditions": [], "medications": [], "goals": [], "profile_id": profile_id}


async def _fake_llm_stream(message: str, context: dict, chunks: list[str]):
    for token in ["안녕", "하세요"]:
        yield token


def _build_service(repository: FakeChatRepository) -> ChatService:
    return ChatService(
        repository=repository,
        llm_stream=_fake_llm_stream,
        health_context=_fake_health_context,
    )


@pytest.mark.asyncio
async def test_응급_키워드가_감지되면_LLM_호출없이_고정_안내만_반환한다():
    repository = FakeChatRepository()
    service = _build_service(repository)

    chunks = [chunk async for chunk in service.stream_message(session_id=1, profile_id=1, message="가슴 통증 있어요")]

    assert len(chunks) == 1
    assert "emergency_fallback" in chunks[0]
    assert EMERGENCY_FALLBACK_MESSAGE in chunks[0]
    assert DISCLAIMER_TEXT in chunks[0]
    assert repository.saved_calls == []


@pytest.mark.asyncio
async def test_응급이_아니면_LLM_스트리밍_후_사용자_어시스턴트_메시지를_모두_저장한다():
    repository = FakeChatRepository()
    service = _build_service(repository)

    chunks = [
        chunk async for chunk in service.stream_message(session_id=1, profile_id=1, message="두통약 뭐가 좋아요?")
    ]

    assert any('"type": "token"' in c for c in chunks)
    assert '"type": "done"' in chunks[-1]
    assert DISCLAIMER_TEXT in chunks[-1]
    assert len(repository.saved_calls) == 2
    assert repository.saved_calls[0][2] == "user"
    assert repository.saved_calls[1][2] == "assistant"
    assert repository.saved_calls[1][3] == "안녕하세요"


@pytest.mark.asyncio
async def test_다른_사용자의_세션에는_접근할_수_없다():
    session = FakeSession(id=1, session_uuid="uuid-1", profile_id=1)
    repository = FakeChatRepository(sessions=[session])
    service = _build_service(repository)

    result = await service.get_authorized_session("uuid-1", profile_id=999)

    assert result is None
