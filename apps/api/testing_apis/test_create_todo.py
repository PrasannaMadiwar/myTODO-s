

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

def test_create_todo_once(authheader):
    response = client.post(
        "/create_todo_once",
        headers= authheader,
        json={
        "title": "string",
        "time": "2026-08-10T09:49:07.345Z",
        "is_completed": False
        }

    )
    assert response.status_code == 201


def test_create_todo_daily(authheader):
    response = client.post(
        "/create_todo_daily",
        headers= authheader,
        json={
        "title": "string",
        "time": "2026-08-10T09:49:07.345Z",
        "is_completed": False
        }

    )
    assert response.status_code == 201


def test_create_todo_weekly(authheader):
    response = client.post(
        "/create_todo_weekly",
        headers= authheader,
        json={
        "title": "string",
        "time": "2026-08-10T09:49:07.345Z",
        "is_completed": False
        }

    )
    assert response.status_code == 201



def test_create_todo_monthly(authheader):
    response = client.post(
        "/create_todo_monthly",
        headers= authheader,
        json={
        "title": "string",
        "time": "2026-08-10T09:49:07.345Z",
        "is_completed": False
        }

    )
    assert response.status_code == 201