def test_user_a_can_access_assigned_vehicle(client):
    # Login as User A
    login_a = client.post("/auth/login", json={"username": "usera", "password": "password123"}).json()
    token_a = login_a["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Record location for vehicle 1
    client.post(
        "/vehicles/1/location",
        json={"latitude": 12.9716, "longitude": 77.5946, "speed": 45.0},
        headers=headers_a
    )

    # 1. Access /me/vehicle
    res_me_veh = client.get("/me/vehicle", headers=headers_a)
    assert res_me_veh.status_code == 200
    assert res_me_veh.json()["vehicle_number"] == "BUS-001"

    # 2. Access /me/vehicle/location
    res_me_loc = client.get("/me/vehicle/location", headers=headers_a)
    assert res_me_loc.status_code == 200
    assert res_me_loc.json()["vehicle_number"] == "BUS-001"
    assert res_me_loc.json()["latitude"] == 12.9716

    # 3. Access direct /vehicles/1 (Assigned)
    res_veh_1 = client.get("/vehicles/1", headers=headers_a)
    assert res_veh_1.status_code == 200


def test_user_a_cannot_access_user_b_vehicle_strict_403(client):
    # Login as User A (assigned to BUS-001 / id: 1)
    login_a = client.post("/auth/login", json={"username": "usera", "password": "password123"}).json()
    token_a = login_a["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Login as User B to record location for vehicle 2
    login_b = client.post("/auth/login", json={"username": "userb", "password": "password123"}).json()
    token_b = login_b["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    client.post(
        "/vehicles/2/location",
        json={"latitude": 12.2958, "longitude": 76.6394, "speed": 55.0},
        headers=headers_b
    )

    # User A requests Vehicle 2 details -> MUST RETURN 403
    res_veh_2 = client.get("/vehicles/2", headers=headers_a)
    assert res_veh_2.status_code == 403
    assert res_veh_2.json()["detail"] == "You are not authorized to access this vehicle"

    # User A requests Vehicle 2 location -> MUST RETURN 403
    res_loc_2 = client.get("/vehicles/2/location", headers=headers_a)
    assert res_loc_2.status_code == 403
    assert res_loc_2.json()["detail"] == "You are not authorized to access this vehicle"

    # User A requests Vehicle 2 history -> MUST RETURN 403
    res_hist_2 = client.get("/vehicles/2/history", headers=headers_a)
    assert res_hist_2.status_code == 403
    assert res_hist_2.json()["detail"] == "You are not authorized to access this vehicle"


def test_user_b_cannot_access_user_a_vehicle_strict_403(client):
    # Login as User B (assigned to BUS-002 / id: 2)
    login_b = client.post("/auth/login", json={"username": "userb", "password": "password123"}).json()
    token_b = login_b["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User B requests Vehicle 1 details -> MUST RETURN 403
    res_veh_1 = client.get("/vehicles/1", headers=headers_b)
    assert res_veh_1.status_code == 403
    assert res_veh_1.json()["detail"] == "You are not authorized to access this vehicle"

    # User B requests Vehicle 1 location -> MUST RETURN 403
    res_loc_1 = client.get("/vehicles/1/location", headers=headers_b)
    assert res_loc_1.status_code == 403
    assert res_loc_1.json()["detail"] == "You are not authorized to access this vehicle"


def test_route_access_authorization(client):
    # Login as User A (Route 1)
    token_a = client.post("/auth/login", json={"username": "usera", "password": "password123"}).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User A can get /me/route
    res_my_route = client.get("/me/route", headers=headers_a)
    assert res_my_route.status_code == 200
    assert res_my_route.json()["name"] == "Route A"

    # User A can access /routes/1
    assert client.get("/routes/1", headers=headers_a).status_code == 200

    # User A cannot access /routes/2 (Route B) -> 403
    res_route_2 = client.get("/routes/2", headers=headers_a)
    assert res_route_2.status_code == 403
    assert res_route_2.json()["detail"] == "You are not authorized to access this route"
