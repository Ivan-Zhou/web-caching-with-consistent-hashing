import requests
from utils import get_master_address

def get_request(url):
	master_address = get_master_address()
	proxies = {
		'http': f'http://{master_address["host"]}:{master_address["port"]}',
	}
	return requests.get(url, proxies=proxies)


if __name__ == '__main__':
	response = get_request('http://example.com')
	print(response)
