from tests.conftest import HEADERS, CUSTOMER_ID, PRODUCT_ID, ORDER_ID


def test_list_orders(client):
    resp = client.get("/api/v1/orders", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_list_orders_by_customer(client):
    resp = client.get(
        f"/api/v1/orders?customer_id={CUSTOMER_ID}",
        headers=HEADERS,
    )
    assert resp.status_code == 200
    orders = resp.json()
    assert len(orders) >= 1
    assert all(o["customer_id"] == CUSTOMER_ID for o in orders)


def test_get_order(client):
    resp = client.get(f"/api/v1/orders/{ORDER_ID}", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "delivered"
    assert data["total_amount"] == 99.98


def test_get_order_not_found(client):
    resp = client.get("/api/v1/orders/nonexistent", headers=HEADERS)
    assert resp.status_code == 404


def test_create_order(client):
    payload = {
        "customer_id": CUSTOMER_ID,
        "product_id": PRODUCT_ID,
        "quantity": 3,
    }
    resp = client.post("/api/v1/orders", json=payload, headers=HEADERS)
    assert resp.status_code == 201
    data = resp.json()
    assert data["quantity"] == 3
    assert data["total_amount"] == 149.97


def test_update_order_status(client):
    payload = {"status": "shipped"}
    resp = client.put(f"/api/v1/orders/{ORDER_ID}", json=payload, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["status"] == "shipped"
