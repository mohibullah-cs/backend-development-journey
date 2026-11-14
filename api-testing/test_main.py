from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test home route
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Authentication API is running"
    }


# Test successful login
def test_login_success():
    response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# Test incorrect password
def test_login_failure():
    response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


# Test protected route without token
def test_protected_route_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401


# Test protected route with valid token
def test_protected_route_with_token():

    login_response = client.post(
        "/token",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "admin"
