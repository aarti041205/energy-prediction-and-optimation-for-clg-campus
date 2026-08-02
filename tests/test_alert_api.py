def test_alerts_endpoint(client):
    response = client.get("/alerts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
