from app.auth.jwt_handler import create_access_token, verify_token


def test_create_and_verify_token():
    token = create_access_token(subject="testuser")
    payload = verify_token(token)
    assert payload["sub"] == "testuser"


def test_verify_token_returns_empty_for_invalid():
    payload = verify_token("not-a-real-token")
    assert payload == {}


def test_verify_token_returns_empty_for_tampered():
    token = create_access_token(subject="testuser")
    tampered = token[:-4] + "XXXX"
    payload = verify_token(tampered)
    assert payload == {}


def test_token_endpoint_returns_jwt(client):
    response = client.post(
        "/api/v1/token",
        json={"username": "demo", "password": "demo"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    payload = verify_token(data["access_token"])
    assert payload["sub"] == "demo"
