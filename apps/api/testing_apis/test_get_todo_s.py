
from apps.api.source.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app=app)

@pytest.fixture
def authheader():
    response = client.post(
        "/login",
        data={
            "username": "Prasanna",
            "password" : "12345"
        }
    )

    assert response.status_code == 200
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}



def test_get_todos(authheader):
    response = client.get(
        "/get_todos/2",
        headers= authheader,
    )

    assert response.status_code in [200]


def test_get_todos_search(authheader):
    response = client.get(
        "/search_todo/s",
        headers= authheader,
    )

    assert response.status_code in [200]