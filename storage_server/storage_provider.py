from flask import Flask, send_from_directory, request
import os
import json
import hashlib
import shutil
import storage_writes

app = Flask(__name__)

# PORT in range 8020 - 8029
PORT = os.environ['SSC_PORT']
USERNAME = os.environ['SSC_USERNAME']
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024


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
    if not storage_writes.replicate(pss['replicas'], str(int(PORT)+10), path, temp_path):
        os.remove(temp_path)
        return 'Not allowed\n', 402
    shutil.move(temp_path, full_path)
    storage_writes.log_update(USERNAME, path, 'write')
    return 'Success\n'


# tested
@app.route('/read/<path:path>', methods=['GET'])
def read(path):
    if '../' in path:
        return 'Forbidden path\n', 401
    return send_from_directory('storage/files/{0}'.format(USERNAME), path, as_attachment=False)


# tested
@app.route('/lsdir/<path:path>', methods=['GET'])
def listdir(path):
    if '../' in path:
        return 'Forbidden path\n', 401
    full_path = 'storage/files/{0}/{1}'.format(USERNAME, path)
    d = []
    try:
        ls = os.scandir(full_path)
        for item in ls:
            c = {}
            c['dir'] = item.is_dir()
            c['name'] = item.name
            c['size'] = item.stat().st_size
            d.append(c)
    except:
        return 'Directory does not exist\n', 404
    return json.dumps(d)

