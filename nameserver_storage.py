
from flask import Flask
from storage_handler import create_handler

flask_ns_storage = Flask(__name__)


@flask_ns_storage.route('/')
def request_index():
    return 'Ok', 200


@flask_ns_storage.route('/alive')
def request_read():
    return create_handler('alive').run()


if __name__ == '__main__':
    flask_ns_storage.run(host='0.0.0.0', port=5010)