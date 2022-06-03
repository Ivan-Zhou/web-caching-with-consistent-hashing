import requests
import fire
from time import time
from utils import get_test_urls, load_image_content, get_section_num, get_webserver_address, get_master_address


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


REQUEST_SLEEP_INTERVAL = 0.5

def get_request(url):
	master_address = get_master_address()

	print("proxy running on host: {}, port: {}".format(master_address["host"], master_address["port"]))
	proxies = {
		'http': f'{master_address["host"]}:{master_address["port"]}',
	}
	try:
		response = requests.get(url, proxies=proxies)
		print("Get response {} for url {}".format(response.status_code, url))
		return response
	except Exception as e:
		print(f"Fail to get response from proxy due to {e}")


def main():
	t_start = time()
	
	webserver_address = get_webserver_address()
	# print("Webserver running on host: {}, port: {}".format(webserver_address["host"], webserver_address["port"]))

	section_num_range = range(0, get_section_num())

	# my_test_urls = ["http://myth58.stanford.edu:6161/1"]

	for number in section_num_range:
		# /{number} number is the section number of webpage 
		url = f"http://{webserver_address['host']}:{webserver_address['port']}/{number}"
		res = get_request(url)	
	t_end = time()
	t_execute = t_end - t_start
	print(f"Finish all {len(section_num_range)} requests in {t_execute} seconds")

# def main():
#     t_start = time()
#     webserver_address = get_webserver_address()
#     section_num_range = range(0, get_section_num())
#     for number in section_num_range:
#         url = f"http://{webserver_address['host']}:{webserver_address['port']}/{number}"
#         res = requests.get(url)	
#         print(f"{url} - {res.status_code}")

#     t_end = time()
#     t_execute = t_end - t_start
#     print(f"Finish all {len(section_num_range)} requests in {t_execute} seconds")

if __name__ == '__main__':
    fire.Fire(main)