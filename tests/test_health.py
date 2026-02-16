def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_schema(client):
    data = client.get("/health").json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_health_no_auth_required(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
