import pytest
from api import app

@pytest.fixture
def client():
    """Provides a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_user(client):
    """Test adding a new user via POST request."""
    response = client.post('/users', json={'name': 'John Doe', 'email': 'john@email.com'})
    assert response.status_code == 201
    assert response.json == {'id': 1, 'name': 'John Doe', 'email': 'john@email.com'}

def test_get_user(client):
    """Test retrieving an existing user by ID."""
    client.post('/users', json={'name': 'Bob Leck', 'email': 'bob@test.com'})
    response = client.get('/users/2')
    assert response.status_code == 200
    assert response.json == {'id': 2, 'name': 'Bob Leck', 'email': 'bob@test.com'}

def test_get_user_not_found(client):
    """Test retrieving a non-existent user."""
    response = client.get('/users/999')
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_add_invalid_user(client):
    """Test adding a user with missing fields."""
    response = client.post('/users', json={'name': 'Jane Doe'})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input"}
