
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




def test_update_todo(authheader):
    response = client.put(
        "/update_todo/1",
        headers= authheader,
        json={
        "title": "string",
        "time": "2026-08-10T09:49:07.345Z",
        "is_completed": False
        }

    )
    assert response.status_code in [404, 201]


def test_update_todo_status(authheader):
    response = client.put(
        "/update_todo_status/1",
        headers= authheader,
        params={
        "is_completed": True
        }
        
    )
    assert response.status_code in [404, 201]



def test_delete_todo(authheader):
    response = client.delete(
        "/delete_todo/1",
        headers= authheader
    )
    assert response.status_code in [404, 204]