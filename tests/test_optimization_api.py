def test_optimization_endpoint(client):
    payload = {
        "Building": "AI Lab",
        "Energy_kWh": 400.0
    }
    response = client.post("/optimize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "total_potential_savings_kwh" in data
    assert "expected_annual_savings_inr" in data
    assert "recommendations" in data
