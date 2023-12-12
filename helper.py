import requests

def check_url(url: str) -> bool:
    """
    Checks if a URL exists by making a HEAD request to the server.

    Args:
        url (str): The URL to check

    Returns:
        bool: True if the URL exists, False otherwise

    Raises:
        requests.RequestException: If the request to the server fails
    """
    try:
        response = requests.head(url)
        return response.status_code == 200  # Status code 200 indicates the URL exists
    except requests.RequestException:
        return False  # Any exception means the URL doesn't exist or is unreachable  # Any exception means the URL doesn't exist or is unreachable
