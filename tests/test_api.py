import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a test client
client = TestClient(app)

def test_register_user():
    # Test user registration
    response = client.post(
        "/register",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    # Test user login
    response = client.post(
        "/token",
        data={
            "username": "test_user",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_task(client, test_user):
    # Log in to get the access token
    login_response = client.post(
        "/token",
        data={
            "username": "test_user",
            "password": "password123"
        }
    )
    access_token = login_response.json()["access_token"]

    # Create a task
    response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending",
            "priority": "High",
            "user_id": 1,
            "category_id": 1
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks(client, test_user):
    # Log in to get the access token
    login_response = client.post(
        "/token",
        data={
            "username": "test_user",
            "password": "password123"
        }
    )
    access_token = login_response.json()["access_token"]

    # Fetch tasks
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()["tasks"], list)

def test_unauthorized_access():
    # Test unauthorized access to a protected endpoint
    response = client.get("/tasks")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_invalid_login():
    # Test login with invalid credentials
    response = client.post(
        "/token",
        data={
            "username": "invalid_user",
            "password": "wrong_password"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"