import requests

def check_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200  # Status code 200 indicates the URL exists
    except requests.RequestException:
        return False  # Any exception means the URL doesn't exist or is unreachable
