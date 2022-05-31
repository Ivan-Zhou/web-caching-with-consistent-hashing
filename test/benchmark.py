import requests
import fire
from time import time
from utils import get_test_urls, load_image_content, get_section_num, get_webserver_address


# def main(n=3):
#     test_urls = get_test_urls(n)
#     n = len(test_urls) # in case number of urls is less than n
#     t_start = time()
#     for i, url in enumerate(test_urls):
#         response = requests.get(url)
#         print(f"{i}: {url} - {response.status_code}")
#     t_end = time()
#     t_execute = t_end - t_start
#     print(f"Finish all {n} requests in {t_execute} seconds")

#TEST fectching contents directly from our own webserver
def main():
    t_start = time()
    webserver_address = get_webserver_address()
    section_num_range = range(0, get_section_num())
    for number in section_num_range:
        url = f"http://{webserver_address['host']}:{webserver_address['port']}/{number}"
        res = requests.get(url)	
        print(f"{url} - {res.status_code}")

    t_end = time()
    t_execute = t_end - t_start
    print(f"Finish all {len(section_num_range)} requests in {t_execute} seconds")

if __name__ == '__main__':
    fire.Fire(main)