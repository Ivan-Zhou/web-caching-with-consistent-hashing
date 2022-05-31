import requests
import threading
from utils import get_master_address, get_webserver_address, get_section_num
from time import time
import pandas as pd
from test.utils import get_test_urls
from time import sleep
REQUEST_SLEEP_INTERVAL = 0.5
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry




# TEST_URLS = [
# 	"http://web.stanford.edu/class/cs110",
#     "http://www.washington.edu",
# 	"http://www.go.com",
# ]


def get_request(url):
	master_address = get_master_address()

	print("proxy running on host: {}, port: {}".format(master_address["host"], master_address["port"]))
	proxies = {
		'http': f'{master_address["host"]}:{master_address["port"]}',
	}
	try:
		# session = requests.Session()
		# retry = Retry(connect=3, backoff_factor=0.5)
		# adapter = HTTPAdapter(max_retries=retry)
		# session.mount('http://', adapter)
		# response = session.get(url, proxies=proxies)
		response = requests.get(url, proxies=proxies)
		print("Get response {} for url {}".format(response.status_code, url))
		return response
	except Exception as e:
		print(f"Fail to get response from proxy due to {e}")



if __name__ == '__main__':
	t_start = time()
	
	webserver_address = get_webserver_address()
	# print("Webserver running on host: {}, port: {}".format(webserver_address["host"], webserver_address["port"]))

	section_num_range = range(0, get_section_num())
	# my_test_urls = ["http://myth58.stanford.edu:6161/1"]

	for number in section_num_range:
		
		
		# /{number} number is the section number of webpage 
		url = f"http://{webserver_address['host']}:{webserver_address['port']}/{number}"
		
		# sleep(REQUEST_SLEEP_INTERVAL)
		res = get_request(url)	
		# print(res.content)
	t_end = time()
	t_execute = t_end - t_start
	print(f"Finish all {len(section_num_range)} requests in {t_execute} seconds")
