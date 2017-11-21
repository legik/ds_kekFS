from flask import Flask
import json
import os
import requests
from filelock import FileLock
from subprocess import Popen
from werkzeug.utils import secure_filename

app = Flask(__name__)

lock = FileLock('mapping.json')


mapping = {}
provider_pool = []
replicator_pool = []
updater_pool = []


@app.route('/init/<int:port>/<username>', methods=['POST'])
def init(port, username):
    username = secure_filename(username)
    lock.acquire()
    if port not in range(8020, 8030):
        return 'Wrong parameters\n'
    if username in mapping:
        return 'Wrong parameters\n'
    try:
        os.mkdir('files/{0}'.format(username), 0o775)
    except:
        pass
    new_provider(port, username)
    new_replicator(port + 10, username)
    mapping['username'] = {'p_port': port, 'r_port': (port + 10)}
    save_state()
    lock.release()
    return 'Success\n'


@app.route('/uneedupdate/<master_address>', methods=['POST'])
def schedule_updates(master_address):
    return 'Success'


def new_updater(port, username):
    return


def new_provider(port, username):
    if username in provider_pool:
        provider_pool[username].terminate()
    new_env = os.environ.copy()
    new_env['FLASK_APP'] = 'storage_provider.py'
    new_env['SSC_PORT'] = str(port)
    new_env['SSC_USERNAME'] = str(username)
    provider_pool[username] = Popen(['flask', 'run', '-h', '0.0.0.0', '-p', str(port)], env=new_env)
    return


def new_replicator(port, username):
    if username in replicator_pool:
        replicator_pool[username].terminate()
    new_env = os.environ.copy()
    new_env['FLASK_APP'] = 'storage_replicator.py'
    new_env['SR_PORT'] = str(port)
    new_env['SR_USERNAME'] = str(username)
    provider_pool[username] = Popen(['flask', 'run', '-h', '0.0.0.0', '-p', str(port)], env=new_env)
    return


def save_state():
    with open('mapping.json', 'w') as f:
        f.write(json.dumps(mapping))
    return


def restore_state():
    lock.acquire()
    with open('mapping.json', 'r') as f:
        mapping = json.loads(f.read())
        for key, value in mapping.items():
            new_provider(value['p_port'], key)
            new_replicator(value['r_port'], key)
    lock.release()
    return


if __name__ == '__main__':
    restore_state()