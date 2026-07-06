"""
통합테스트 규칙 (test_auth_router.py와 동일): status_code와 응답 형태만 확인, 로직 재검증은 안 함.
세부 로직 검증은 이미 test_chat_service.py(단위테스트)에서 끝났다.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_채팅_메시지_전송_정상응답():
    response = client.post(
        "/chat/sessions/10/messages",
        params={"profile_id": 1},
        json={"message": "두통약 뭐가 좋아요?"},
    )

    assert response.status_code == 200
    assert len(response.text) > 0


def test_채팅_메시지_전송_응급키워드는_고정안내를_반환한다():
    response = client.post(
        "/chat/sessions/10/messages",
        params={"profile_id": 1},
        json={"message": "가슴 통증 있어요"},
    )

    assert response.status_code == 200
    assert "119" in response.text
