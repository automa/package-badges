def test_healthcheck_endpoint(client):
    """Test the health/live endpoint returns a 200 OK status."""
    response = client.get("/health/live")

    assert response.status_code == 200

    assert response.content == b""
