import pytest


@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "securepassword123",
        "password_confirmation": "securepassword123",
    }


@pytest.fixture
def test_user_login():
    return {
        "email": "test@example.com",
        "password": "securepassword123",
    }


@pytest.mark.asyncio
async def test_signup_success(client, test_user):
    response = await client.post("/auth/signup", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signup_duplicate_email(client, test_user):
    await client.post("/auth/signup", json=test_user)
    response = await client.post("/auth/signup", json=test_user)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_signup_password_mismatch(client):
    data = {
        "email": "mismatch@example.com",
        "password": "password123",
        "password_confirmation": "differentpassword123",
    }
    response = await client.post("/auth/signup", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client, test_user, test_user_login):
    await client.post("/auth/signup", json=test_user)
    response = await client.post("/auth/login", json=test_user_login)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user):
    await client.post("/auth/signup", json=test_user)
    response = await client.post(
        "/auth/login",
        json={"email": test_user["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    response = await client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authenticated(client, test_user):
    signup_resp = await client.post("/auth/signup", json=test_user)
    token = signup_resp.json()["access_token"]
    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401
