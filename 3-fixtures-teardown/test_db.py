import pytest
from db import DataBase

@pytest.fixture
def db():
    """
    Provide a fresh database instance for each test and clear it after.
    
    This pattern shows how to use setup and teardown via 'yield'.
    """
    database = DataBase()
    yield database
    database.data.clear()  # teardown step

def test_add_user(db):
    """Test adding a user to the database."""
    db.add_user(1, "Alice")
    assert db[1] == "Alice"

def test_add_existing_user(db):
    """Test that adding a duplicate user raises ValueError."""
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match="User ID already exists"):
        db.add_user(1, "Bob")

def test_delete_user(db):
    """Test deleting a user from the database."""
    db.add_user(1, "Alice")
    del db[1]
    assert db[1] is None
