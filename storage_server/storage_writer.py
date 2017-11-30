from flask import Flask, request
import os
import shutil
import json
import hashlib
from werkzeug.utils import secure_filename

import storage_writes

# PORT in range 8030 - 8039
PORT = os.environ['SR_PORT']
USERNAME = os.environ['SR_USERNAME']

pusher = None

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024


# tested
@app.route('/mkdir/<path:path>', methods=['POST'])
def mkdir(path):
    if '../' in path:
        return 'Forbidden path\n', 401
    if storage_writes.mkdir(USERNAME, path) is not True:
        return 'Directory does not exist\n', 404
    return 'Success\n'


# tested
@app.route('/rmdir/<path:path>', methods=['POST'])
def rmdir(path):
    if '../' in path:
        return 'Forbidden path\n', 401
    if storage_writes.rmdir(USERNAME, path) is not True:
        return 'Directory does not exist\n', 404
    return 'Success\n'


# tested
@app.route('/write/<path:path>', methods=['POST'])
def write(path):
    if '../' in path:
        return 'Forbidden path\n', 404
    if 'file' not in request.files:
        return 'File is not provided\n'
    f = request.files['file']
    if f.filename == '':
        return 'File is not provided\n'
    full_path = storage_writes.rename_on_exist(USERNAME, path)
    path = full_path.replace('storage/files/{0}/'.format(USERNAME), '', 1)
    temp_path = 'storage/files/tmp/{0}/{1}'.format(USERNAME, hashlib.sha256(path.encode('utf-8')).hexdigest())
    try:
        f.save(temp_path)
    except:
        return 'File is already processing\n', 404
    try:
        pss = storage_writes.ask_nameserver(os.stat(temp_path).st_size, path, USERNAME)
    except:
        os.remove(temp_path)
        return 'Operation is not allowed 1\n', 501
    if 'status' not in pss or pss['status'] != 'allowed' or len(pss['replicas']) not in [0, 1, 2]:
        os.remove(temp_path)
        return json.dumps(pss), 401
    if not storage_writes.replicate(pss['replicas'], str(int(PORT)), path, temp_path):
        os.remove(temp_path)
        return 'Not allowed\n', 402
    shutil.move(temp_path, full_path)
    storage_writes.log_update(USERNAME, path, 'write')
    return 'Success\n'


# tested
@app.route('/replicate/<path:path>', methods=['POST'])
def replicate(path):
    if '../' in path:
        return 'Forbidden path\n', 401
    if 'file' not in request.files:
        return 'File is not provided\n', 401
    f = request.files['file']
    if f.filename == '':
        return 'File is not provided\n', 401
    full_path = storage_writes.get_full_path(USERNAME, path)
    try:
        f.save(full_path)
        storage_writes.log_update(USERNAME, path, 'write')
    except:
        return 'Write fail\n', 500
    return 'Success\n'


# tested
@app.route('/delete/<path:path>', methods=['POST'])
def delete(path):
    if '../' in path:
        return 'Forbidden path\n', 401
    if storage_writes.delete(USERNAME, path) is not True:
        return 'File does not exist\n', 404
    return 'Success\n'


# tested
@app.route('/rename/<new_name>/<path:path>', methods=['POST'])
def rename(new_name, path):
    new_name = secure_filename(new_name)
    if '../' in path:
        return 'Forbidden path\n', 401
    if storage_writes.rename(USERNAME, path, new_name) is not True:
        return 'Directory does not exist\n', 404
    return 'Success\n'
