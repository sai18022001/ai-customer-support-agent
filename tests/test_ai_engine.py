from unittest.mock import patch, MagicMock

from app.services.ai_engine import AIEngine


def _make_mock_client(response_text):
    mock_message = MagicMock()
    mock_message.content = response_text

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


def test_classify_message_success():
    engine = AIEngine()
    json_text = '{"intent": "billing", "sentiment": "negative", "confidence": 0.88, "suggested_actions": ["create_case"], "requires_escalation": false}'
    mock_client = _make_mock_client(json_text)

    with patch.object(engine, "_get_client", return_value=mock_client):
        result = engine.classify_message("Why was I charged twice?")

    assert result["intent"] == "billing"
    assert result["sentiment"] == "negative"
    assert result["confidence"] == 0.88
    assert "create_case" in result["suggested_actions"]


def test_classify_message_fallback_on_error():
    engine = AIEngine()
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API error")

    with patch.object(engine, "_get_client", return_value=mock_client):
        result = engine.classify_message("something")

    assert result["intent"] == "general"
    assert result["confidence"] == 0.5


def test_generate_response_success():
    engine = AIEngine()
    mock_client = _make_mock_client("I can help you with that billing issue.")

    with patch.object(engine, "_get_client", return_value=mock_client):
        result = engine.generate_response(
            message="Why was I charged twice?",
            customer_context={"customer_name": "Alice", "customer_tier": "premium", "recent_orders": []},
            conversation_history=[],
            classification={"intent": "billing", "sentiment": "negative"},
        )

    assert "billing" in result.lower()


def test_generate_response_fallback_on_error():
    engine = AIEngine()
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API error")

    with patch.object(engine, "_get_client", return_value=mock_client):
        result = engine.generate_response(
            message="Help",
            customer_context={},
            conversation_history=[],
            classification={},
        )

    assert "apologize" in result.lower()
