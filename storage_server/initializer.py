from flask import Flask
import json
import os
import shutil
import time
from subprocess import Popen
from werkzeug.utils import secure_filename
import hashlib
from config import NAMESERVER_1
import requests

provider_pool = {}
replicator_pool = {}
updaters_pool = {}
pushers_poll = {}
mapping = {}
nonces = {}
heartbeat = ''
updating = 'updating'
update_failed = 'update_failed'
update_status = {updating: False, update_failed: False}
print(update_status[update_failed])

MAPPING = 'storage/mapping.json'

PORT = 8010


def new_provider(port, username):
    if username in provider_pool:
        provider_pool[username].terminate()
    new_env = os.environ.copy()
    new_env['FLASK_APP'] = 'storage_reader.py'
    new_env['SSC_PORT'] = str(port)
    new_env['SSC_USERNAME'] = str(username)
    provider_pool[username] = Popen(['flask', 'run', '-h', '0.0.0.0', '-p', str(port)], env=new_env)
    return


def new_replicator(port, username):
    if username in replicator_pool:
        replicator_pool[username].terminate()
    new_env = os.environ.copy()
    new_env['FLASK_APP'] = 'storage_writer.py'
    new_env['SR_PORT'] = str(port)
    new_env['SR_USERNAME'] = str(username)
    replicator_pool[username] = Popen(['flask', 'run', '-h', '0.0.0.0', '-p', str(port)], env=new_env)
    return


def new_pusher(username):
    if username in pushers_poll:
        pushers_poll[username].terminate()
    new_env = os.environ.copy()
    new_env['FLASK_APP'] = 'storage_pusher.py'
    new_env['SPUSH_PORT'] = str(mapping[username]['r_port'])
    new_env['SPUSH_USERNAME'] = str(username)
    pushers_poll[username] = Popen(['flask', 'run', '-h', '0.0.0.0', '-p', str(int(mapping[username]['r_port']) + 10)], env=new_env)
    return


def new_updater(username, port, master_address, nonce):
    updaters_pool[username] = Popen(['python', 'storage_updater.py', username, str(port), str(master_address), str(nonce)])
    return


def save_state():
    with open(MAPPING, 'w') as f:
        f.write(json.dumps(mapping))
    return


def restore_state():
    if not os.path.isdir('storage/files'):
        os.mkdir('storage/files')
    e = open('storage/empty', 'w')
    e.write('{}')
    e.close()
    if not os.path.isdir('storage/files/tmp'):
        os.mkdir('storage/files/tmp')
    if not os.path.isfile(MAPPING):
        e = open(MAPPING, 'w')
        e.write('{}')
        e.close()
    global mapping
    with open(MAPPING, 'r') as f:
        for line in f:
            mapping = json.loads(line)
            for key, value in mapping.items():
                new_provider(value['p_port'], key)
                new_replicator(value['r_port'], key)
    save_state()
    return


def launch_heartbeat():
    global heartbeat
    heartbeat = Popen(['python', 'heartbeat.py'])
    return


app = Flask(__name__)

restore_state()
launch_heartbeat()


@app.route('/init/<int:port>/<username>', methods=['POST'])
def init(port, username):
    username = secure_filename(username)
    if port not in range(8020, 8030):
        return 'Wrong parameters\n', 401
    if username in mapping and mapping[username]['p_port'] != port:
        return 'Wrong parameters\n', 401
    try:
        shutil.rmtree('storage/files/{0}'.format(username))
        shutil.rmtree('storage/files/tmp/{0}'.format(username))
    except:
        pass
    os.mkdir('storage/files/{0}'.format(username), 0o775)
    os.mkdir('storage/files/tmp/{0}'.format(username), 0o775)
    f = open('storage/files/{0}_last_update'.format(username), 'w')
    f.write('0')
    f.close()
    f = open('storage/files/{0}_update.log'.format(username), 'w')
    f.write('')
    f.close()
    f = open('storage/files/{0}_filelock'.format(username), 'w')
    f.write('')
    f.close()
    new_provider(port, username)
    new_replicator(port + 10, username)
    if username not in mapping:
        mapping[username] = {'init_number': 1, 'p_port': port, 'r_port': (port + 10)}
    else:
        mapping[username]['init_number'] = mapping[username]['init_number'] + 1
    save_state()
    return 'Success\n'


@app.route('/kill/<username>', methods=['POST'])
def kill(username):
    username = secure_filename(username)
    if username not in mapping:
        return 'Wrong parameters', 401
    provider_pool[username].terminate()
    replicator_pool[username].terminate()
    os.remove('storage/files/{0}_last_update'.format(username))
    os.remove('storage/files/{0}_update.log'.format(username))
    os.remove('storage/files/{0}_filelock'.format(username))
    shutil.rmtree('storage/files/{0}'.format(username))
    shutil.rmtree('storage/files/tmp/{0}'.format(username))
    del mapping[username]
    save_state()
    return 'Success\n'


@app.route('/uneedupdate/<master_address>', methods=['POST'])
def schedule_updates(master_address):
    if update_status[updating] is True:
        return 'Success\n'
    update_status[updating] = True
    url = 'http://{0}:8010/mapping'.format(master_address)
    try:
        req = requests.get(url)
    except:
        return 'Fail\n', 404
    new_mapping = req.json()
    ll = []
    for item in mapping:
        if item not in new_mapping:
            ll.append(item)
            continue
    for item in ll:
        kill(item)
    ll = []
    for item in new_mapping:
        if item not in mapping:
            ll.append(item)
            continue
        if new_mapping[item]['init_number'] > mapping[item]['init_number']:
            ll.append(item)
            mapping[item]['init_number'] = new_mapping[item]['init_number'] - 1
            continue
    for item in ll:
        init(new_mapping[item]['p_port'], item)
    for key, value in mapping.items():
        nonces[key] = hashlib.sha256((str(time.clock()) + key).encode('utf-8')).hexdigest()
        new_updater(key, value['r_port'], master_address, nonces[key])
    if len(nonces) == 0:
        return 'Updated\n'
    return 'Success\n'


@app.route('/mapping', methods=['GET'])
def give_mapping():
    return json.dumps(mapping)


@app.route('/updated/<user>/<nonce>', methods=['POST'])
def updated(user, nonce):
    if nonces[user] != nonce:
        print('Bad nonce')
        return 'Fail\n', 400
    del nonces[user]
    if len(nonces) == 0 and update_status[update_failed] is False:
        print('Branch 1')
        try:
            requests.post('http://{0}/updated'.format(NAMESERVER_1))
            update_status[updating] = False
        except Exception as e:
            print(e)
            update_status[updating] = False
            return 'Fail\n', 400
    if len(nonces) == 0 and update_status[update_failed] is True:
        print('Branch 2')
        update_status[updating] = False
        update_status[update_failed] = False
    return 'Success\n'


@app.route('/update_failed/<user>/<nonce>', methods=['POST'])
def update_failed_fun(user, nonce):
    if nonces[user] != nonce:
        return 'Fail\n', 400
    del nonces[user]
    del updaters_pool[user]
    update_status[update_failed] = True
    if len(nonces) == 0:
        update_status[updating] = False
        update_status[update_failed] = False
    return 'Success\n'


@app.route('/create_pusher/<username>', methods=['GET'])
def give_pusher(username):
    if username not in mapping:
        return 'Wrong parameters', 404
    new_pusher(username)
    return 'Success\n', 200


@app.route('/kill_pusher/<username>', methods=['GET'])
def kill_pusher(username):
    if username not in mapping:
        return 'Wrong parameters', 404
    pushers_poll[username].terminate()
    return 'Success\n'
