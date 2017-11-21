
import requests
import config_s

def send_live():
    while True:
        requests.get('http://{0}/alive'.format(config.NAMESERVER))
        wait(2)


if __name__ == '__main__':
    send_live()