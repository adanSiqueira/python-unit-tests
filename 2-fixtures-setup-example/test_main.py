import pytest
from main import UserManager

@pytest.fixture
def user_manager():
    """Creates a fresh instance of UserManager for each test."""
    return UserManager()

def test_add_user(user_manager):
    """Test adding a new user."""
    assert user_manager.add_user("john_doe", "john@example.com") is True
    assert user_manager["john_doe"] == "john@example.com"

def test_add_existing_user(user_manager):
    """Test attempting to add a duplicate user."""
    user_manager.add_user("john_doe", "john@example.com")
    with pytest.raises(ValueError, match="User already exists"):
        user_manager.add_user("john_doe", "another@example.com")

def test_get_nonexistent_user(user_manager):
    """Test retrieving non-existent user."""
    assert user_manager["nonexistent"] is None
