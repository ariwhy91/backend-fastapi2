# tests/test_integration.py
def test_login_dengan_password_salah_mengembalikan_401(client, db_session):
    import models
    from security import hash_password
 
    user = models.User(
        name="Budi",
        username="budi",
        email="budi@example.com",
        password_hash=hash_password("passwordbenar"),
        saldo=0,
        role="user",
    )
    db_session.add(user)
    db_session.commit()
 
    response = client.post(
        "/auth/login",
        data={"username": "budi", "password": "passwordsalah"},
    )
 
    assert response.status_code == 401

# tests/test_integration.py (lanjutan)
def _buat_user_dan_token(client, db_session):
    import models
    from security import hash_password, verify_password
 
    user = models.User(
        name="Siti", username="siti",
        email="siti@example.com",
        password_hash=hash_password("rahasia123"),
        saldo=100000, role="user",
    )
    db_session.add(user)
    db_session.commit()
 
    login_resp = client.post(
        "/auth/login",
        data={"username": "siti", "password": "rahasia123"},
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
 
 
def test_orders_saya_dengan_token_valid_mengembalikan_200(client, db_session):
    headers = _buat_user_dan_token(client, db_session)
    response = client.get("/orders/saya", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
 
 
def test_agregasi_produk_mengembalikan_200_dan_data_terkelompok(client, db_session):
    import models
    headers = _buat_user_dan_token(client, db_session)
 
    db_session.add_all([
        models.Order(user_id=1, produk="Mouse", jumlah=1, total=50000),
        models.Order(user_id=1, produk="Mouse", jumlah=1, total=50000),
    ])
    db_session.commit()
 
    response = client.get("/orders/aggregasi/produk", headers=headers)
 
    assert response.status_code == 200
    data = response.json()
    assert any(row["produk"] == "Mouse" and row["jumlah_pesanan"] == 2 for row in data)
