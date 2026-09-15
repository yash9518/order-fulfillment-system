import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rbac_customer_cannot_create_product():
    # 1. Register and login as customer
    client.post("/auth/register", json={"email": "cust_test@example.com", "password": "password123", "role": "customer"})
    login_res = client.post("/auth/login", data={"username": "cust_test@example.com", "password": "password123"})
    token = login_res.json()["access_token"]

    # 2. Customer attempts to create product -> must return 403 Forbidden
    res = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Forbidden Item", "price": 99.0, "stock": 5}
    )
    assert res.status_code == 403
    assert res.json()["detail"] == "Admin privileges required to perform this action"

def test_rbac_admin_can_create_product():
    # 1. Register and login as admin
    client.post("/auth/register", json={"email": "admin_test@example.com", "password": "password123", "role": "admin"})
    login_res = client.post("/auth/login", data={"username": "admin_test@example.com", "password": "password123"})
    token = login_res.json()["access_token"]

    # 2. Admin attempts to create product -> must return 201 Created
    res = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Admin Only Item", "price": 49.0, "stock": 10}
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Admin Only Item"