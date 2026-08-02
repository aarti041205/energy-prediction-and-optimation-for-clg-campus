def test_analytics_endpoint(client):
    response = client.get("/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_energy" in data
    assert "avg_energy" in data
    assert "total_cost" in data
    assert "total_carbon" in data
