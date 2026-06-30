from tests.conftest import HEADERS


def test_overview_metrics(client):
    resp = client.get("/api/v1/analytics/overview", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_sessions" in data
    assert "resolution_rate" in data
    assert "avg_satisfaction" in data


def test_intent_distribution(client):
    resp = client.get("/api/v1/analytics/intents", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "intents" in data
    assert isinstance(data["intents"], list)
