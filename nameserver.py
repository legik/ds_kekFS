
from flask import Flask
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from client_handler import create_handler
from os import urandom
from functools import wraps


app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            return 'You need to login first\n', 401
    return wrap


@app.route('/')
def request_index():
    return ''


@app.route('/login', methods=['POST'])
def request_login():
    return create_handler('login').run(request, session)


@app.route('/logout')
@login_required
def request_logout():
    session.clear()
    return ''


@app.route('/read/<file>')
@login_required
def request_read(file):
    return create_handler('read').run(file)


@app.route('/write/<file>')
@login_required
def request_write(file):
    return create_handler('write').run(file)


@app.route('/delete/<file>')
@login_required
def request_delete(file):
    return create_handler('delete').run(file)


@app.route('/size/<file>')
@login_required
def request_size(file):
    return create_handler('size').run(file)


@app.route('/mkdir/<file>')
@login_required
def request_mkdir(file):
    return create_handler('mkdir').run(file)


@app.route('/rmdir/<file>')
@login_required
def request_rmdir(file):
    return create_handler('rmdir').run(file)


if __name__ == '__main__':
    app.secret_key = urandom(12)
    app.run()