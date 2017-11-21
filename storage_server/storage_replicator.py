from flask import Flask
import json
import filelock
import requests
import storage_writes

PORT = os.environ['SSC_PORT']
USERNAME = os.environ['SSC_USERNAME']

@app.route('/delete/<path:path>', methods=['POST'])
def delete(path):
    if '../' in path:
        return 'Forbidden path\n'
    full_path = 'files/{0}'.format(path)
    try:
        os.remove(full_path)
    except:
        return 'File does not exist\n'
    return 'Success\n'

@app.route('/rmdir/<path:path>', methods=['POST'])
def rmdir(path):
    if '../' in path:
        return 'Forbidden path\n'
    full_path = 'files/{0}'.format( path)
    try:
        shutil.rmtree(full_path)
    except:
        return 'Directory does not exist\n'
    return 'Success\n'

@app.route('/read/<path:path>', methods=['GET'])
def read(path):
    if '../' in path:
        return 'Forbidden path\n'
    return send_from_directory('files/', path, as_attachment=True)

