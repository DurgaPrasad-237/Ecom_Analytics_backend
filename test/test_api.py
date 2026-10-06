from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_api_starts():
    response = client.get("/")
    assert response.status_code == 200