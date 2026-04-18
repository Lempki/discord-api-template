import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DISCORD_API_SECRET", "test-secret")

from api_template.main import app  # noqa: E402

client = TestClient(app)
AUTH = {"Authorization": "Bearer test-secret"}
WRONG_AUTH = {"Authorization": "Bearer wrong"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "discord-api-template"


def test_echo_no_auth():
    response = client.post("/template/echo", json={"text": "hello"})
    assert response.status_code == 403


def test_echo_wrong_auth():
    response = client.post("/template/echo", json={"text": "hello"}, headers=WRONG_AUTH)
    assert response.status_code == 401


def test_echo():
    response = client.post("/template/echo", json={"text": "hello"}, headers=AUTH)
    assert response.status_code == 200
    assert response.json()["text"] == "hello"
