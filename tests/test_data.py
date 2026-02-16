def test_data_returns_200_with_token(client, auth_headers):
    response = client.get("/api/v1/data", headers=auth_headers)
    assert response.status_code == 200


def test_data_returns_unauthorized_without_token(client):
    response = client.get("/api/v1/data")
    assert response.status_code in (401, 403)


def test_data_rejects_invalid_token(client):
    headers = {"Authorization": "Bearer invalid-token-value"}
    response = client.get("/api/v1/data", headers=headers)
    assert response.status_code == 401


def test_data_response_schema(client, auth_headers):
    data = client.get("/api/v1/data", headers=auth_headers).json()
    assert "items" in data
    assert "total" in data
    assert data["total"] == 3
    assert data["items"][0]["name"] == "Widget A"
