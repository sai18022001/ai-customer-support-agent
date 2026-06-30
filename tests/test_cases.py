from tests.conftest import HEADERS, CUSTOMER_ID


def test_create_case(client):
    payload = {
        "customer_id": CUSTOMER_ID,
        "subject": "Cannot access dashboard",
        "description": "Getting 403 error when trying to open the analytics page",
        "priority": "high",
        "category": "technical",
    }
    resp = client.post("/api/v1/cases", json=payload, headers=HEADERS)
    assert resp.status_code == 201
    data = resp.json()
    assert data["subject"] == "Cannot access dashboard"
    assert data["status"] == "open"
    assert data["priority"] == "high"


def test_list_cases(client):
    client.post(
        "/api/v1/cases",
        json={
            "customer_id": CUSTOMER_ID,
            "subject": "Test case",
            "description": "For listing",
        },
        headers=HEADERS,
    )
    resp = client.get("/api/v1/cases", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_update_case(client):
    create_resp = client.post(
        "/api/v1/cases",
        json={
            "customer_id": CUSTOMER_ID,
            "subject": "Update test",
            "description": "Will be updated",
        },
        headers=HEADERS,
    )
    case_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/api/v1/cases/{case_id}",
        json={"status": "resolved", "resolution": "Fixed the permissions"},
        headers=HEADERS,
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["status"] == "resolved"
    assert data["resolution"] == "Fixed the permissions"


def test_get_case_not_found(client):
    resp = client.get("/api/v1/cases/nonexistent", headers=HEADERS)
    assert resp.status_code == 404
