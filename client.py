import requests
from utils import get_master_address
TEST_URLS = [
    "http://www.washington.edu",
	"http://www.go.com",
	"http://web.stanford.edu/class/cs110"
	# http://ecosimulation.com/cgi-bin/longAccessTime.py?time=4
]

def get_request(url):
	master_address = get_master_address()
	print("proxy running on host: {}, port: {}".format(master_address["host"], master_address["port"]))
	proxies = {
		'http': f'http://{master_address["host"]}:{master_address["port"]}',
	}
	return requests.get(url, proxies=proxies)


if __name__ == '__main__':
	for url in TEST_URLS:
		print("{} forward request to proxy".format(url))
		response = get_request(url)
		print("get response back {}".format(response))
	print("All URLs got tested")
       
	


