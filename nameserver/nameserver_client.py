from functools import wraps
from os import urandom
from flask import Flask
from flask import request
from flask import session

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nameserver.client_handler import create_handler
from db import sql

flask_ns_client = Flask(__name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' not in request.cookies:
            return 'You need to login first', 403
        else:
            user_name = request.cookies['user']
            user = sql.User.query.filter_by(alias=str(user_name)).first()
            if not user:
                return 'Not valid credentials', 401
            else:
                if user.session == request.cookies['auth']:
                    return f(*args, **kwargs)
                else:
                    return 'You need to login first\n', 401
    return wrap


@flask_ns_client.route('/')
def request_index():
    return ''


@flask_ns_client.route('/register/<username>/<password>', methods=['POST'])
def register(username, password):
    return create_handler('register').run(username, password)


@flask_ns_client.route('/login/<username>/<password>', methods=['POST'])
def request_login(username, password):
    return create_handler('login').run(username, password, session)


@flask_ns_client.route('/logout')
@login_required
def request_logout():
    return create_handler('logout').run(session)


@flask_ns_client.route('/read/<name>/', defaults={'file_name': ''}, methods=['GET'])
@flask_ns_client.route('/read/<name>/<path:file_name>', methods=['GET'])
@login_required
def request_read(name, file_name):
    return create_handler('read').run(name, file_name)


@flask_ns_client.route('/write/<name>/<path:file_name>', methods=['POST'])
@login_required
def request_write(name, file_name):
    return create_handler('write').run(name, file_name)


@flask_ns_client.route('/delete/<name>/<path:file_name>', methods=['POST'])
@login_required
def request_delete(name, file_name):
    return create_handler('delete').run(name, file_name)


@flask_ns_client.route('/size/<name>/<path:file_name>', methods=['GET'])
@login_required
def request_size(name, file_name):
    return create_handler('size').run(name, file_name)


@flask_ns_client.route('/mkdir/<name>/<path:file_name>', methods=['POST'])
@login_required
def request_mkdir(name, file_name):
    return create_handler('mkdir').run(name, file_name)


@flask_ns_client.route('/rmdir/<name>/<path:file_name>', methods=['POST'])
@login_required
def request_rmdir(name, file_name):
    return create_handler('rmdir').run(name, file_name)


@flask_ns_client.route('/init/<name>', methods=['POST'])
@login_required
def request_init(name):
    return create_handler('init').run(name)


@flask_ns_client.route('/alive', methods=['POST'])
def request_test():
    r = request.form['alive']
    return create_handler('alive').run(r)


@flask_ns_client.route('/submitted/<size>/<path:file_name>', methods=['GET'])
def request_submitted(size, file_name):
    return 'ok', 200


if __name__ == '__main__':
    flask_ns_client.secret_key = urandom(12)
    flask_ns_client.run(host='0.0.0.0', port=5000, debug=False, threaded=False)
