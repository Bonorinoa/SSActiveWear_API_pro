# tests/test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_read_root():
    """Tests if the root endpoint is accessible."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the SS Activewear Catalog API!"}

def test_get_products_pagination():
    """Tests the default pagination returns 50 items."""
    response = requests.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 50 # Default page_size

def test_get_products_filtering():
    """Tests if filtering by category works correctly."""
    params = {"category": "Headwear"}
    response = requests.get(f"{BASE_URL}/api/products", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0 # Should find at least one result
    # Check if all returned items match the filter
    for item in data:
        assert item['baseCategory'] == 'Headwear'

def test_get_filters_endpoint():
    """Tests if the filters endpoint returns the correct structure."""
    response = requests.get(f"{BASE_URL}/api/filters")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "colors" in data
    assert "brands" in data
    assert isinstance(data["categories"], list)