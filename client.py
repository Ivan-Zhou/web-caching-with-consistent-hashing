import requests
import threading
from utils import get_master_address
from datetime import datetime
TEST_URLS = [
    "http://www.washington.edu",
	"http://www.go.com",
	"http://web.stanford.edu/class/cs110"
	
]

def get_request(url):
	master_address = get_master_address()
	print("proxy running on host: {}, port: {}".format(master_address["host"], master_address["port"]))
	proxies = {
		'http': f'http://{master_address["host"]}:{master_address["port"]}',
	}
	response = requests.get(url, proxies=proxies)
	print("Get response {} for url {}".format(response.status_code, url))
	# print(response.text)



if __name__ == '__main__':
	threads = []
	t_start = datetime.now()
	for url in TEST_URLS:
		# Each thread handling one request
		t = threading.Thread(target = get_request(url))
		t.start()
		threads.append(t)	
	for t in threads:
		t.join()
	t_end = datetime.now()
	t_execute = t_end - t_start
	print("Finish all requests, t = {}".format(t_execute))
       
	


