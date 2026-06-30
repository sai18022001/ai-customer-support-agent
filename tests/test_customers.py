from tests.conftest import HEADERS, CUSTOMER_ID


def test_list_customers(client):
    resp = client.get("/api/v1/customers", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_customer(client):
    resp = client.get(f"/api/v1/customers/{CUSTOMER_ID}", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test User"
    assert data["tier"] == "premium"


def test_get_customer_not_found(client):
    resp = client.get("/api/v1/customers/nonexistent", headers=HEADERS)
    assert resp.status_code == 404


def test_create_customer(client):
    payload = {
        "name": "New User",
        "email": "newuser@test.com",
        "tier": "basic",
    }
    resp = client.post("/api/v1/customers", json=payload, headers=HEADERS)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "New User"
    assert data["email"] == "newuser@test.com"


def test_update_customer(client):
    payload = {"company": "Updated Corp"}
    resp = client.put(
        f"/api/v1/customers/{CUSTOMER_ID}",
        json=payload,
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert resp.json()["company"] == "Updated Corp"


def test_unauthorized_access(client):
    resp = client.get("/api/v1/customers")
    assert resp.status_code == 401

    resp = client.get(
        "/api/v1/customers",
        headers={"X-API-Key": "wrong-key"},
    )
    assert resp.status_code == 401
