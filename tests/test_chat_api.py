def test_chat_endpoint(client):
    payload = {
        "question": "What is the average energy consumption of the AI Lab?"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "confidence" in data
    assert "sources" in data
