"""
Unit tests for db.py using pytest and pytest-mock.

Here, we demonstrate *mocking* external dependencies — in this case,
the sqlite3 database connection — so our tests run fast, deterministically,
and without requiring an actual database file.
"""

import pytest
from db import save_user


def test_save_user_success(mocker):
    """
    Test that save_user correctly connects to the database,
    inserts data, commits, and closes the connection.

    Mocking ensures no real database operations occur.
    """
    # Mock sqlite3.connect() to return a fake connection object
    mock_conn = mocker.patch("sqlite3.connect")
    mock_cursor = mock_conn.return_value.cursor.return_value

    # Call the function under test
    save_user("Alice", 30)

    # Assertions: verify the function called DB methods properly
    mock_conn.assert_called_once_with("users.db")
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        ("Alice", 30)
    )
    mock_conn.return_value.commit.assert_called_once()
    mock_conn.return_value.close.assert_called_once()


def test_save_user_database_error(mocker):
    """
    Test that save_user propagates a database error correctly.
    """
    mock_conn = mocker.patch("sqlite3.connect")
    mock_cursor = mock_conn.return_value.cursor.return_value

    # Simulate a database error when executing the query
    mock_cursor.execute.side_effect = Exception("DB write failed")

    with pytest.raises(Exception, match="DB write failed"):
        save_user("Bob", 25)

    # Ensure it attempted to connect but failed during execution
    mock_conn.assert_called_once_with("users.db")
    mock_cursor.execute.assert_called_once()
