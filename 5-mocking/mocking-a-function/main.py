import requests

def get_weather(city):
    """
    Fetch weather data for a given city from a public API.

    Args:
        city (str): City name.

    Returns:
        dict: JSON weather response.

    Raises:
        ValueError: If city not found or API returns an error.
    """
    response = requests.get(f"http://api.weatherapi.com/v1/{city}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("City not found or API error")
