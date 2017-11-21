import requests
import config

while True:
	requests.get('http://{0}/alive'.format(config.NAMESERVER))
	wait(2)