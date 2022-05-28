import requests
import fire
from datetime import datetime
from utils import get_test_urls


def main(n=3):
    test_urls = get_test_urls(n)
    n = len(test_urls) # in case number of urls is less than n
    t_start = datetime.now()
    for i, url in enumerate(test_urls):
        response = requests.get(url)
        print(f"{i}: {url} - {response.status_code}")
    t_end = datetime.now()
    t_execute = t_end - t_start
    print(f"Finish all {n} requests, t = {t_execute}")


if __name__ == '__main__':
    fire.Fire(main)