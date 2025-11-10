"""
A simple example demonstrating how a function interacts
with a database using sqlite3.

In production, this function connects to a database,
inserts a user record, commits the transaction,
and then closes the connection.

In testing, however, we will mock sqlite3.connect()
to avoid creating an actual database file.
"""

import sqlite3

def save_user(name: str, age: int) -> None:
    """
    Saves a user record in the database.

    Args:
        name (str): The user's name.
        age (int): The user's age.

    Raises:
        sqlite3.Error: If any database operation fails.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (name, age),
    )

    conn.commit()
    conn.close()
