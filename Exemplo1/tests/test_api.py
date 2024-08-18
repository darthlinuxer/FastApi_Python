import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.service_item import ItemService

client = TestClient(app)

@pytest.fixture
def item_service():
    return ItemService()

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "A test item", "price": 10.0, "qtty": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert data["price"] == 10.0
    assert data["qtty"] == 5
    assert "id" in data

def test_create_item_duplicate_name():
    client.post("/items/", json={"name": "Duplicate Item", "price": 10.0, "qtty": 5})
    response = client.post("/items/", json={"name": "Duplicate Item", "price": 15.0, "qtty": 3})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_read_item():
    create_response = client.post("/items/", json={"name": "Read Test", "price": 20.0, "qtty": 1})
    item_id = create_response.json()["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Read Test"
    assert data["price"] == 20.0
    assert data["qtty"] == 1

def test_read_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_item():
    create_response = client.post("/items/", json={"name": "Update Test", "price": 30.0, "qtty": 2})
    item_id = create_response.json()["id"]
    
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated Item", "description": "An updated item", "price": 35.0, "qtty": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["description"] == "An updated item"
    assert data["price"] == 35.0
    assert data["qtty"] == 3

def test_update_item_not_found():
    response = client.put(
        "/items/9999",
        json={"name": "Non-existent Item", "price": 40.0, "qtty": 1}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_delete_item():
    create_response = client.post("/items/", json={"name": "Delete Test", "price": 50.0, "qtty": 1})
    item_id = create_response.json()["id"]
    
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verify the item is deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_delete_item_not_found():
    response = client.delete("/items/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_create_item_invalid_price():
    response = client.post("/items/", json={"name": "Invalid Price", "price": -10.0, "qtty": 1})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_item_invalid_quantity():
    response = client.post("/items/", json={"name": "Invalid Quantity", "price": 10.0, "qtty": -1})
    assert response.status_code == 422  # Unprocessable Entity

def test_update_item_partial_price_and_description():
    create_response = client.post("/items/", json={"name": "Partial Update Test", "price": 60.0, "qtty": 5})
    item_id = create_response.json()["id"]
    
    response = client.put(
        f"/items/{item_id}", 
        json={"name": "Partially Updated Item", "price": 65.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Partially Updated Item"
    assert data["price"] == 65.0
    assert data["qtty"] == 5  # Should remain unchanged

def test_update_item_partial_qtty():
    create_response = client.post("/items/", json={"name": "Partial Update Test", "price": 60.0, "qtty": 5})
    item_id = create_response.json()["id"]
    
    response = client.put(
        f"/items/{item_id}", 
        json={"qtty": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Partial Update Test" # Should remain unchanged
    assert data["price"] == 60.0 # Should remain unchanged
    assert data["qtty"] == 2  


def test_get_all_items():
    # Clear all items first
    response = client.get("/items/")
    for item in response.json():
        client.delete(f"/items/{item['id']}")

    # Create a few items
    client.post("/items/", json={"name": "Item 1", "price": 10.0, "qtty": 1})
    client.post("/items/", json={"name": "Item 2", "price": 20.0, "qtty": 2})
    client.post("/items/", json={"name": "Item 3", "price": 30.0, "qtty": 3})

    # Get all items
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert any(item["name"] == "Item 1" for item in data)
    assert any(item["name"] == "Item 2" for item in data)
    assert any(item["name"] == "Item 3" for item in data)

def test_update_item_invalid_data():
    create_response = client.post("/items/", json={"name": "Invalid Update Test", "price": 70.0, "qtty": 5})
    item_id = create_response.json()["id"]
    
    response = client.put(
        f"/items/{item_id}", 
        json={"name": "Invalid Update", "price": -5.0, "qtty": 5}
    )
    assert response.status_code == 422
    assert "greater than" in response.json()["detail"][0]["msg"]

    response = client.put(
        f"/items/{item_id}", 
        json={"name": "Invalid Update", "price": 70.0, "qtty": -1}
    )
    assert response.status_code == 422
    assert "greater than or equal to" in response.json()["detail"][0]["msg"]