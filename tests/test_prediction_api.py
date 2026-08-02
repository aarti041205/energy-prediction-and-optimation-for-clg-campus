def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data

def test_prediction_endpoint(client):
    payload = {
        "Building": "AI Lab",
        "Building_Type": "Laboratory",
        "Temperature": 28.0,
        "Humidity": 65.0,
        "Hour": 14,
        "Day": 15,
        "Month": 8,
        "Weekend": 0,
        "Holiday": 0,
        "Equipment_Load": 0.85
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_energy_kwh" in data
    assert data["predicted_energy_kwh"] > 0
    assert "confidence_score" in data
    assert "id" in data
