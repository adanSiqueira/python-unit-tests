class DataBase:
    """
    Simulate a basic in-memory user database with add, get, and delete operations.
    """

    def __init__(self):
        """Initialize the database with an empty dictionary."""
        self.data = {}

    def add_user(self, user_id, name):
        """Add a user to the database."""
        if user_id in self.data:
            raise ValueError("User ID already exists")
        self.data[user_id] = name

    def __getitem__(self, user_id):
        """Retrieve user name by ID."""
        return self.data.get(user_id, None)

    def __delitem__(self, user_id):
        """Delete a user by ID."""
        if user_id in self.data:
            del self.data[user_id]
        else:
            raise KeyError("User ID not found")
