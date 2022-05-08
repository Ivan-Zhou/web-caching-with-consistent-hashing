# importing the requests library
import requests

URL = "http://0.0.0.0:8080"
PARAMS = {"test": "this is a test"}


def get_request(url, params):
    print(f"GET request to {url} with params {params}")
    try:
        r = requests.get(url=url, params=params)
        print(f"Response status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def post_request(url, params):
    print(f"POST request to {url} with params {params}")
    try:
        r = requests.post(url=url, params=params)
        print(f"Response status code: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    get_request(url=URL, params=PARAMS)
    post_request(url=URL, params=PARAMS)


if __name__ == "__main__":
    main()
