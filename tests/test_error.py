def test_nonexistent_route_returns_404(client):
    """Test that accessing a non-existent route returns a 404 status code."""
    response = client.get("/unhandled-route")

    assert response.status_code == 404

    assert "detail" in response.json()
    assert response.json()["detail"] == "Not Found"
