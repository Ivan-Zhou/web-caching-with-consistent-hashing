import requests
import threading
from utils import get_master_address
from time import time
import pandas as pd
from test.utils import get_test_urls


TEST_URLS = [
	"http://web.stanford.edu/class/cs110",
    "http://www.washington.edu",
	"http://www.go.com",
]


def get_request(url):
	master_address = get_master_address()

	print("proxy running on host: {}, port: {}".format(master_address["host"], master_address["port"]))
	proxies = {
		'http': f'{master_address["host"]}:{master_address["port"]}',
	}
	try:
		response = requests.get(url, proxies=proxies)
		print("Get response {} for url {}".format(response.status_code, url))
	except Exception as e:
		print(f"Fail to get response from proxy due to {e}")



if __name__ == '__main__':
	# threads = []
	t_start = time()
	test_urls = get_test_urls(n=3)
	for url in test_urls:
		# Each thread handling one request
		get_request(url)
	t_end = time()
	t_execute = t_end - t_start
	print(f"Finish all {len(test_urls)} requests in {t_execute} seconds")
