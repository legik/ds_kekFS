
from flask import Flask
from flask import request
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nameserver.storage_handler import create_handler

flask_ns_storage = Flask(__name__)


@flask_ns_storage.route('/')
def request_index():
    return 'Ok', 200


@flask_ns_storage.route('/alive')
def request_read():
    return create_handler('alive').run(request.environ['REMOTE_ADDR'])


@flask_ns_storage.route('/submitted/<size>/<path:file_name>', methods=['GET'])
def request_submitted(size, file_name):
    return create_handler('submitted').run(size, file_name)


@flask_ns_storage.route('/updated')
def request_updated_replic():
    return create_handler('updated').run(request.environ['REMOTE_ADDR'])


@flask_ns_storage.route('/update_failed')
def request_update_failed():
    return create_handler('update_failed').run(request.environ['REMOTE_ADDR'])


if __name__ == '__main__':
    flask_ns_storage.run(host='0.0.0.0', port=5010)