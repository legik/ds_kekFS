import requests
import sys
import storage_writes
from time import sleep

# tested
username = sys.argv[1]
port = sys.argv[2]
master_addr = sys.argv[3]
nonce = sys.argv[4]
version = storage_writes.get_data_version(username)

str = 'Updater for {}:{} - '.format(username, port)

print(str + 'started')


def do_update():
    url = 'http://{0}:{1}/create_pusher/{2}'.format(master_addr, 8010, username)
    print(url)
    try:
        r = requests.get(url)
    except Exception:
        print(str + 'cannot create pusher')
        return False
    if r.status_code != 200:
        return False
    sleep(3)
    url = 'http://{0}:{1}/push_updates/{2}'.format(master_addr, int(port) + 10, version)
    try:
        r = requests.get(url)
    except Exception:
        print(str + 'pusher fail pusher')
        return False
    if r.status_code != 200:
        print(r.status_code)
        return False
    sleep(3)
    url = 'http://{0}:{1}/kill_pusher/{2}'.format(master_addr, port, username)
    try:
        r = requests.get(url)
    except:
        pass
    return True


def send_update_done():
    url = 'http://localhost:8010/updated/{0}/{1}'.format(username, nonce)
    try:
        r = requests.post(url)
    except:
        return False


def send_update_failed():
    url = 'http://localhost:8010/update_failed/{0}/{1}'.format(username, nonce)
    try:
        r = requests.post(url)
    except:
        return False


if do_update():
    send_update_done()
else:
    send_update_failed()


