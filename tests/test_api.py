from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}


def test_analyze_rejects_wrong_protocol():
    response = client.post(
        "/v1/analyze",
        json={"url": "ftp://example.com"},
    )

    assert response.status_code == 403


def test_analyze_requires_url():
    response = client.post("/v1/analyze", json={})

    assert response.status_code == 422