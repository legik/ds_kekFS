
import os
import json

from storage_server.common_operation import command_mkdir
from storage_server.common_operation import command_delete
from storage_server.common_operation import command_rmdir
from flask import Flask

app = Flask(__name__)


PORT = os.environ['SSC_PORT']
USERNAME = os.environ['SSC_USERNAME']

class ChangedList:
    def __init__(self):
        self.list_operation = []

    def add_new_operation(self, operation, user, path):
        item = {'op':operation, 'user': user, 'path': path}
        self.list_operation.append(item)


    def get_list(self):
        return self.list_operation

    def get_version(self):
        return len(self.list_operation)

    def load_from_json(self, json):
        self.list_operation = json.loads(json)

    def get_json(self):
        return json.dumps(self.list_operation)



@app.route('/delete/<path:path>', methods=['POST'])
def delete(path):
    if '../' in path:
        return 'Forbidden path\n'

    if command_delete(path) is not True:
        return 'File does not exist\n'

    return 'Success\n'


@app.route('/rmdir/<path:path>', methods=['POST'])
def rmdir(path):
    if '../' in path:
        return 'Forbidden path\n'

    if command_rmdir(path) is not True:
        return 'Directory does not exist\n'

    return 'Success\n'


@app.route('/mkdir/<path:path>', methods=['POST'])
def rmdir(path):
    if '../' in path:
        return 'Forbidden path\n'

    if command_mkdir(path) is not True:
        return 'Directory does not exist\n'

    return 'Success\n'


@app.route('/read/<path:path>', methods=['GET'])
def read(path):
    if '../' in path:
        return 'Forbidden path\n'

    #return send_from_directory('files/', path, as_attachment=True)
    return ''


@app.route('/changedlistversion')
def changedlistversion():
    return 'Success\n', 200


if __name__ == '__main__':
    l = []
    l.append({'op':'del', 'user': 'aa', 'path': 'path'})
    l.append({'op': 'rm', 'user': 'aa', 'path': 'path'})
    l.append({'op': 'name', 'user': 'aa', 'path': 'path'})
    l.append({'op': 'del', 'user': 'aa', 'path': 'path'})

    print(json.dumps(l))