"""
통합테스트 규칙:
- Router는 TestClient로 '진짜 HTTP 요청을 보낸 것처럼' 테스트한다.
- 여기서는 status_code와 응답 JSON 형태가 API 명세(OpenAPI)와 일치하는지만 확인한다.
- 세부 로직 검증은 이미 test_nickname_service.py(단위테스트)에서 끝났으므로 여기서 반복하지 않는다.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_닉네임_중복확인_API_정상응답():
    response = client.get("/auth/nickname/check", params={"nickname": "완전히새로운닉네임"})

    assert response.status_code == 200
    assert response.json() == {"available": True}


def test_닉네임_중복확인_API_이미존재하는닉네임():
    response = client.get("/auth/nickname/check", params={"nickname": "admin"})

    assert response.status_code == 200
    assert response.json() == {"available": False}
