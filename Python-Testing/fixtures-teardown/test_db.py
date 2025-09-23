import pytest
from db import DataBase

@pytest.fixture
def db():
    database = DataBase()
    yield database
    database.data.clear()

def test_add_user(db):
    db.add_user(1, "Alice")
    assert db[1] == "Alice"

def test_add_existing_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match="User ID already exists"):
        db.add_user(1, "Bob")

def test_delete_user(db):
    db.add_user(1, "Alice")
    del db[1]
    assert db[1] is None