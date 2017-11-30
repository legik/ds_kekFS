from flask import Flask, send_from_directory
import os
import json

app = Flask(__name__)

# PORT in range 8020 - 8029
PORT = os.environ['SSC_PORT']
USERNAME = os.environ['SSC_USERNAME']
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024


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

