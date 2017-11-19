
from flask import Flask
from flask import session
from flask import request

from client_handler import create_handler
from os import urandom
from functools import wraps


flask_ns_client = Flask(__name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            return 'You need to login first\n', 401
    return wrap

@flask_ns_client.route('/')
def request_index():
    return ''


@flask_ns_client.route('/login', methods=['POST'])
def request_login():
    return create_handler('login').run(request, session)


@flask_ns_client.route('/logout')
@login_required
def request_logout():
    return create_handler('logout').run(session)


@flask_ns_client.route('/read/<file>')
@login_required
def request_read(file):
    return create_handler('read').run(file)


@flask_ns_client.route('/write/<file>')
@login_required
def request_write(file):
    return create_handler('write').run(file)


@flask_ns_client.route('/delete/<file>')
@login_required
def request_delete(file):
    return create_handler('delete').run(file)


@flask_ns_client.route('/size/<file>')
@login_required
def request_size(file):
    return create_handler('size').run(file)


@flask_ns_client.route('/mkdir/<file>')
@login_required
def request_mkdir(file):
    return create_handler('mkdir').run(file)


@flask_ns_client.route('/rmdir/<file>')
@login_required
def request_rmdir(file):
    return create_handler('rmdir').run(file)


if __name__ == '__main__':
    flask_ns_client.secret_key = urandom(12)
    flask_ns_client.run(host='0.0.0.0', port=5000)