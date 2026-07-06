"""
통합테스트 규칙 (CODING_RULES.md §4): TestClient로 status_code/응답 형태만 확인, 로직 재검증은
이미 test_chat_service.py(단위테스트)에서 끝났으므로 여기서 반복하지 않는다.

app.main.app 대신 chat_routers만 얹은 가벼운 앱을 쓴다 — app.main의 lifespan은 실제 MySQL
연결을 시도하므로, 라우팅/응답 형태만 확인하는 이 테스트에는 불필요한 인프라 의존이다.
get_current_user/get_service를 오버라이드해 실제 DB/OpenAI 호출 없이 결정적으로 통과한다.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.apis.v1 import chat_routers
from app.core.dependencies import get_current_user
from app.services.chat_service import ChatService
from app.tests.test_chat_service import FakeChatRepository, _fake_health_context, _fake_llm_stream

_router_app = FastAPI()
_router_app.include_router(chat_routers.router)

_repository = FakeChatRepository()
_service = ChatService(_repository, llm_stream=_fake_llm_stream, health_context=_fake_health_context)

_router_app.dependency_overrides[get_current_user] = lambda: {"sub": "1"}
_router_app.dependency_overrides[chat_routers.get_service] = lambda: _service

client = TestClient(_router_app)


def test_세션_생성_정상응답():
    response = client.post("/sessions")

    assert response.status_code == 201
    assert "session_id" in response.json()


def test_메시지_전송_정상응답():
    session_id = client.post("/sessions").json()["session_id"]

    response = client.post(f"/sessions/{session_id}/messages", json={"message": "두통약 뭐가 좋아요?"})

    assert response.status_code == 200
    assert '"type": "done"' in response.text


def test_존재하지_않는_세션에_메시지를_보내면_404():
    response = client.post("/sessions/no-such-session/messages", json={"message": "안녕"})

    assert response.status_code == 404
