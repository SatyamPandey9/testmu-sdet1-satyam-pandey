import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

class TestAPI:

    def test_get_users(self):
        """GET /users - successful response aana chahiye"""
        response = requests.get(f"{BASE_URL}/users")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_single_user(self):
        """GET /users/1 - single user data aana chahiye"""
        response = requests.get(f"{BASE_URL}/users/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "email" in data

    def test_create_post(self):
        """POST /posts - naya post create hona chahiye"""
        payload = {
            "title": "Test Post",
            "body": "This is a test post body",
            "userId": 1
        }
        response = requests.post(f"{BASE_URL}/posts", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Post"

    def test_update_post(self):
        """PUT /posts/1 - post update hona chahiye"""
        payload = {
            "id": 1,
            "title": "Updated Post",
            "body": "Updated body",
            "userId": 1
        }
        response = requests.put(f"{BASE_URL}/posts/1", json=payload)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Post"

    def test_delete_post(self):
        """DELETE /posts/1 - post delete hona chahiye"""
        response = requests.delete(f"{BASE_URL}/posts/1")
        assert response.status_code == 200

    def test_invalid_endpoint(self):
        """Invalid endpoint pe 404 aana chahiye"""
        response = requests.get(f"{BASE_URL}/invalidendpoint")
        assert response.status_code == 404

    def test_schema_validation(self):
        """Response schema sahi hona chahiye"""
        response = requests.get(f"{BASE_URL}/users/1")
        data = response.json()
        required_fields = ["id", "name", "username", "email", "address", "phone"]
        for field in required_fields:
            assert field in data, f"Field '{field}' missing from response"