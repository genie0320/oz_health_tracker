from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_confirm_데모_API_정상응답_형태():
    response = client.post("/recognition/confirm-demo", params={"drug_name": "자몽주스"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "confirmed"
    assert isinstance(body["guide_cards"], list)
    assert len(body["guide_cards"]) >= 1
    assert "disclaimer" in body["guide_cards"][0]
