class UserManager:
    """
    Simple user manager that stores usernames and emails in memory.
    """

    def __init__(self):
        """Initialize an empty user dictionary."""
        self.users = {}

    def add_user(self, username, email):
        """
        Add a new user.

        Args:
            username (str): The username to add.
            email (str): User's email address.
        
        Raises:
            ValueError: If the username already exists.
        
        Returns:
            bool: True if added successfully.
        """
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = email
        return True

    def __getitem__(self, username):
        """
        Get email address for a username.

        Args:
            username (str): Username to look up.
        
        Returns:
            str or None: Email if user exists, else None.
        """
        return self.users.get(username, None)
