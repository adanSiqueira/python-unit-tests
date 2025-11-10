import requests

class APIClient:
    """Simulate an external API client."""
    
    def get_user_data(self, user_id):
        """Fetch user data from an external API."""
        response = requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


class UserService:
    """Service that uses the API client to fetch and process user data."""

    def __init__(self, api_client):
        """Initialize with an API client dependency."""
        self.api_client = api_client

    def get_username(self, user_id):
        """Return the username in uppercase."""
        user_data = self.api_client.get_user_data(user_id)
        return user_data['name'].upper()
