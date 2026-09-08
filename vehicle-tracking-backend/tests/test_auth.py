def test_login_success(client):
    response = client.post("/auth/login", json={"username": "usera", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    response = client.post("/auth/login", json={"username": "usera", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={"username": "nonexistent", "password": "password123"})
    assert response.status_code == 401


def test_get_current_user_profile(client):
    # Login first
    login_res = client.post("/auth/login", json={"username": "usera", "password": "password123"})
    token = login_res.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "usera"
    assert user_data["email"] == "usera@example.com"
    assert user_data["vehicle_id"] == 1


def test_unauthenticated_request_rejected(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
