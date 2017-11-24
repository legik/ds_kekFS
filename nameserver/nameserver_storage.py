
from flask import Flask
from flask import request
from nameserver.storage_handler import create_handler

flask_ns_storage = Flask(__name__)


@flask_ns_storage.route('/')
def request_index():
    return 'Ok', 200


@flask_ns_storage.route('/alive')
def request_read():
    remote_addr = request.environ['REMOTE_ADDR']
    return create_handler('alive').run(remote_addr)


if __name__ == '__main__':
    flask_ns_storage.run(host='0.0.0.0', port=5010)