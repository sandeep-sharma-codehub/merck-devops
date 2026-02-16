import pytest
from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    token = create_access_token(subject="demo")
    return {"Authorization": f"Bearer {token}"}
