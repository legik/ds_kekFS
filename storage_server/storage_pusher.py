from flask import Flask, request
import storage_writes
import requests
import os
import json

USERNAME = os.environ['SPUSH_USERNAME']
PORT = os.environ['SPUSH_PORT']  # writer in range 8030-8039

app = Flask(__name__)


# tested
@app.route('/push_updates/<int:version>', methods=['GET'])
def push_updates(version):
    writes = {}  # {'old_name': 'new_name', }
    update_list = storage_writes.get_update_list(USERNAME, version)
    while len(update_list) > 0:
        for item in update_list:
            if item['operation'] == 'write':
                writes[item['path']] = item['path']
            elif item['operation'] == 'rename_file':
                if item['path'] in writes:
                    writes[item['path']] = item['new_path']
            elif item['operation'] == 'rename_dir':
                for k in writes:
                    a = os.path.commonpath([k, item['path']])
                    if a != '':
                        writes[k] = k.replace(a, item['new_path'], 1)
        for item in update_list:
            version = item['id']
            if item['operation'] == 'mkdir':
                url = 'http://{0}:{1}/mkdir/{2}'.format(request.remote_addr, PORT, item['path'])
                r = requests.post(url)
            elif item['operation'] == 'rmdir':
                url = 'http://{0}:{1}/rmdir/{2}'.format(request.remote_addr, PORT, item['path'])
                r = requests.post(url)
            elif item['operation'] == 'delete':
                url = 'http://{0}:{1}/delete/{2}'.format(request.remote_addr, PORT, item['path'])
                r = requests.post(url)
            elif item['operation'] == 'write':
                url = 'http://{0}:{1}/replicate/{2}'.format(request.remote_addr, PORT, item['path'])
                print(url)
                file_full_path = storage_writes.get_full_path(USERNAME, writes[item['path']])
                try:
                    f = {'file': open(file_full_path, 'rb')}
                except:
                    file_full_path = 'storage/empty'
                    f = {'file': open(file_full_path, 'rb')}
                try:
                    r = requests.post(url, files=f)
                    if r.status_code != 200:
                        return 'Bad request', 502
                except:
                    return json.dumps({url: file_full_path}), 503
            elif item['operation'] == 'rename_dir' or item['operation'] == 'rename_file':
                url = 'http://{0}:{1}/rename/{2}/{3}'.format(request.remote_addr, PORT, item['new_name'], item['path'])
                r = requests.post(url)
            else:
                return 'Fatal error\n', 500
        update_list = storage_writes.get_update_list(USERNAME, version)
    return 'Success\n'
