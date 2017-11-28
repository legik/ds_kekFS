from flask import Flask, request
import os
from subprocess import Popen
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


@app.route('/give_pusher', methods=['GET'])
def give_pusher():
    global pusher
    if pusher is not None:
        pusher.terminate()
        pusher = None
    new_env = os.environ.copy()
    new_env['FLASK_APP'] = 'storage_pusher.py'
    new_env['SPUSH_PORT'] = str(PORT)
    new_env['SPUSH_USERNAME'] = str(USERNAME)
    pusher = Popen(['flask', 'run', '-h', '0.0.0.0', '-p', str(int(PORT)+10)], env=new_env)
    return 'Success\n', 200


@app.route('/kill_pusher', methods=['GET'])
def kill_pusher():
    global pusher
    if pusher is None:
        return 'Success\n'
    pusher.terminate()
    pusher = None
    return 'Success\n'
