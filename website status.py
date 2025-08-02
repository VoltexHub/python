import requests # pip install requests

def check(url):
    try:
        response = requests.get(url)
        print(f"{url} is UP Status Code: {response.status_code}")
    except requests.ConnectionError:
        print(f"{url} is DOWN")

check("https://website.com")
