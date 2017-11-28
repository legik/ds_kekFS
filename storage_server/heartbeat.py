from config import NAMESERVER_1
import requests
import time

print(" * Heartbeat is running")
while True:
    url = 'http://{0}/alive'.format(NAMESERVER_1)
    try:
        r = requests.get(url)
    except:
        pass
    time.sleep(3)
