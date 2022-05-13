import requests

proxies = {
	'http': 'http://myth56.stanford.edu:30657'
}

url = 'http://example.com'

response = requests.get(url, proxies=proxies)

print(response)