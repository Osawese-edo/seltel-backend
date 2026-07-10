import pytest


@pytest.fixture
def test_product():
    return {
        "name": "Test Product",
        "description": "A test product description",
        "price": 29.99,
        "category": "electronics",
        "in_stock": True,
    }


@pytest.fixture
def test_user():
    return {
        "email": "product_tester@example.com",
        "password": "securepassword123",
        "password_confirmation": "securepassword123",
    }


@pytest.mark.asyncio
async def test_create_product(client, test_product):
    response = await client.post("/api/v1/products/", json=test_product)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_product["name"]
    assert data["price"] == test_product["price"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_products(client, test_product):
    await client.post("/api/v1/products/", json=test_product)
    response = await client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_product(client, test_product):
    create_resp = await client.post("/api/v1/products/", json=test_product)
    product_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_product["name"]


@pytest.mark.asyncio
async def test_get_product_not_found(client):
    response = await client.get("/api/v1/products/999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_product_invalid_id(client):
    response = await client.get("/api/v1/products/invalid-id")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_product(client, test_product):
    create_resp = await client.post("/api/v1/products/", json=test_product)
    product_id = create_resp.json()["id"]

    update_data = {"name": "Updated Product", "price": 49.99}
    response = await client.put(f"/api/v1/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 49.99


@pytest.mark.asyncio
async def test_update_product_not_found(client):
    response = await client.put("/api/v1/products/999999", json={"name": "Updated"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_product(client, test_product):
    create_resp = await client.post("/api/v1/products/", json=test_product)
    product_id = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/products/{product_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_not_found(client):
    response = await client.delete("/api/v1/products/999999")
    assert response.status_code == 404
