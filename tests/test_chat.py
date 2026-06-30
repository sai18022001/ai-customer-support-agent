from unittest.mock import patch

from tests.conftest import HEADERS, CUSTOMER_ID

MOCK_CLASSIFICATION = {
    "intent": "order_inquiry",
    "sentiment": "neutral",
    "confidence": 0.92,
    "suggested_actions": ["lookup_customer"],
    "requires_escalation": False,
}


@patch("app.services.ai_engine.ai_engine.classify_message", return_value=MOCK_CLASSIFICATION)
@patch("app.services.ai_engine.ai_engine.generate_response", return_value="I can help with your order!")
def test_send_message(mock_gen, mock_classify, client):
    payload = {
        "customer_id": CUSTOMER_ID,
        "message": "What is the status of my recent order?",
    }
    resp = client.post("/api/v1/chat", json=payload, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["reply"] == "I can help with your order!"
    assert data["detected_intent"] == "order_inquiry"
    assert data["was_escalated"] is False
    assert "session_id" in data


@patch("app.services.ai_engine.ai_engine.classify_message", return_value=MOCK_CLASSIFICATION)
@patch("app.services.ai_engine.ai_engine.generate_response", return_value="Sure, let me check.")
def test_multi_turn_conversation(mock_gen, mock_classify, client):
    resp1 = client.post(
        "/api/v1/chat",
        json={"customer_id": CUSTOMER_ID, "message": "Hi, I need help"},
        headers=HEADERS,
    )
    session_id = resp1.json()["session_id"]

    resp2 = client.post(
        "/api/v1/chat",
        json={
            "customer_id": CUSTOMER_ID,
            "session_id": session_id,
            "message": "Check my order please",
        },
        headers=HEADERS,
    )
    assert resp2.status_code == 200
    assert resp2.json()["session_id"] == session_id


@patch("app.services.ai_engine.ai_engine.classify_message", return_value=MOCK_CLASSIFICATION)
@patch("app.services.ai_engine.ai_engine.generate_response", return_value="Checking...")
def test_get_session_history(mock_gen, mock_classify, client):
    resp = client.post(
        "/api/v1/chat",
        json={"customer_id": CUSTOMER_ID, "message": "Hello"},
        headers=HEADERS,
    )
    session_id = resp.json()["session_id"]

    history_resp = client.get(f"/api/v1/chat/sessions/{session_id}", headers=HEADERS)
    assert history_resp.status_code == 200
    data = history_resp.json()
    assert len(data["conversation"]) == 2
    assert data["conversation"][0]["role"] == "customer"
    assert data["conversation"][1]["role"] == "agent"


ESCALATION_CLASSIFICATION = {
    "intent": "escalate",
    "sentiment": "angry",
    "confidence": 0.95,
    "suggested_actions": ["escalate_to_human"],
    "requires_escalation": True,
}


@patch("app.services.ai_engine.ai_engine.classify_message", return_value=ESCALATION_CLASSIFICATION)
@patch("app.services.ai_engine.ai_engine.generate_response", return_value="Connecting you to a human agent.")
def test_escalation(mock_gen, mock_classify, client):
    resp = client.post(
        "/api/v1/chat",
        json={
            "customer_id": CUSTOMER_ID,
            "message": "This is ridiculous! I want to speak to a manager!",
        },
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert resp.json()["was_escalated"] is True


def test_chat_invalid_customer(client):
    resp = client.post(
        "/api/v1/chat",
        json={"customer_id": "nonexistent", "message": "Hello"},
        headers=HEADERS,
    )
    assert resp.status_code == 404
