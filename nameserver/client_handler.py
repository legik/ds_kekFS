from db import sql
import requests
from flask import make_response
import random
import string


order = 0
sql.Cluster.query.all()


class Handler:
    def __init__(self):
        pass

    def run(self, *args):
        pass


class HandlerRegister(Handler):
    def __init__(self):
        super(HandlerRegister, self).__init__()

    def run(self, *args):
        username = args[0]
        password = args[1]
        if not sql.User.query.filter_by(alias=str(username)).first():
            try:
                users_count = sql.db.session.query(sql.User).count()
                port = self.choose_port(users_count)
                cluster = self.choose_cluster(users_count)
                user = sql.User(alias=str(username), password=str(password), cluster=cluster, port=port, size=200000)
                create_handler('init').run(username)
                sql.db.session.add(user)
                sql.db.session.commit()
                return 'User successfully registered', 200
            except:
                return 'Wrong request parameters', 400
        else:
            return 'User already exist', 400

    def choose_port(self, count):
        return int(8020 + count % 10)

    def choose_cluster(self, count):
        return int(count / 10 + 1)


class HandlerLogin(Handler):
    def __init__(self):
        super(HandlerLogin, self).__init__()

    def run(self, *args):
        username = args[0]
        password = args[1]
        session = args[2]
        registered_user = sql.User.query.filter_by(alias=str(username), password=str(password)).first()
        if registered_user is None:
            return 'Username or Password is invalid', 401
        else:
            s = string.ascii_lowercase + string.digits + string.ascii_uppercase
            cookie = ''.join(random.sample(s, 40))
            registered_user.session = str(cookie)
            sql.db.session.commit()
            session['user'] = registered_user.alias
            session['auth'] = cookie
            resp = make_response('Logged in successfully', 200)
            resp.set_cookie('user', registered_user.alias)
            resp.set_cookie('auth', cookie)
            return resp


class HandlerLogout(Handler):
    def __init__(self):
        super(HandlerLogout, self).__init__()

    def run(self, *args):
        session = args[0]
        session.clear()
        return 'logout', 200


class HandlerRead(Handler):
    def __init__(self):
        super(HandlerRead, self).__init__()

    def run(self, *args):
        user_name = args[0]
        path = args[1] if len(args) == 2 else ''
        print('HandlerRead is started. user: {} file: {}'.format(user_name, path))
        user = sql.User.query.filter_by(alias=str(user_name)).first()
        if not user:
            return 'User does not exist', 400

        if not sql.File.query.filter_by(name=str('/' + user_name + '/' + path)).first():
            return 'File not found', 404
        else:
            try:
                servers = user.tenant
                port = user.port
                ip_main = '{}:{}'.format(servers.mains.address, port)
                ip_second_1 = '{}:{}'.format(servers.seconds1.address, port)
                ip_second_2 = '{}:{}'.format(servers.seconds2.address, port)
                order_array = [ip_main, ip_second_1, ip_second_2]
                json_answer = '{{ "servers" : [ "{}", "{}","{}" ] }}'.format(order_array[order % 3],
                                                                             order_array[(order + 1) % 3],
                                                                             order_array[(order + 2) % 3])
                self.increment()
                return json_answer, 200
            except:
                return 'Wrong request parameters', 400

    def increment(self):
        global order
        if order < 2:
            order = order + 1
        else:
            order = 0


class HandlerWrite(Handler):
    def __init__(self):
        super(HandlerWrite, self).__init__()

    def run(self, *args):
        alias = args[0]
        path = args[1]
        print('HandlerWrite is started. user: {} file: {}'.format(alias, path))
        user = sql.User.query.filter_by(alias=str(alias)).first()
        if not user:
            return 'Wrong request parameters', 400
        try:
            servers = user.tenant
            port = user.port
            ip_main = servers.mains.address
            json_answer = '{{ "servers" : [ "{}:{}" ] }}'.format(ip_main, port)
            return json_answer
        except:
            return 'Wrong request parameters', 400


class HandlerDelete(Handler):
    def __init__(self):
        super(HandlerDelete, self).__init__()
        pass

    def run(self, *args):
        alias = args[0]
        path = args[1]
        print('HandlerDeleteFile is started. user: {} file: {}'.format(alias, path))
        user = sql.User.query.filter_by(alias=str(alias)).first()
        if not user:
            return 'Wrong request parameters', 400
        port = user.port
        client_request = 'delete/{}/{}'.format(alias, path)
        answer = create_handler('request').run(alias, client_request, port)
        s = '/{}/{}'.format(alias, path)
        if answer == 200:
            for f in sql.db.session.query(sql.File).filter(sql.File.name == s).all():
                if f.owner == user:
                    sql.db.session.delete(f)
            sql.db.session.commit()
            return 'Success', 200
        else:
            return 'Wrong request parameters', 401


class HandlerSize(Handler):
    def __init__(self):
        super(HandlerSize, self).__init__()

    def run(self, *args):
        alias = args[0]
        path = args[1]
        print('HandlerDelete is started. user: {} file: {}'.format(alias, path))
        user = sql.User.query.filter_by(alias=str(alias)).first()
        if not user:
            return 'Wrong request parameters', 400
        filter = '/{}/{}'.format(alias, path)
        file = sql.File.query.filter_by(name=filter).first()
        if not file:
            return 'File not found', 404
        else:
            try:
                return '{{ "size" : ' + str(file.size) + ' }}'
            except:
                return 'Wrong request parameters', 400


# TODO: увеличивать size
class HandlerMkDir(Handler):
    def __init__(self):
        super(HandlerMkDir, self).__init__()

    def run(self, *args):
        alias = args[0]
        path = args[1]
        print('HandlerMkDir is started. user: {} directory: {}'.format(alias, path))
        user = sql.User.query.filter_by(alias=str(alias)).first()
        if not user:
            return 'Wrong request parameters', 400
        port = user.port
        client_request = 'mkdir/{}/{}'.format(alias, path)
        answer = create_handler('request').run(alias, client_request, port)
        s = '/{}/{}'.format(alias, path)
        if answer == 200:
            f = sql.File(name=str(path), size=0, user_id=user.id)
            sql.db.session.add(f)
            sql.db.session.commit()
            return 'Success', 200
        else:
            return 'Wrong request parameters', 401


#TODO: vsem po spisku udalyat/dobavlyat
class HandlerRmDir(Handler):
    def __init__(self):
        super(HandlerRmDir, self).__init__()

    def run(self, *args):
        alias = args[0]
        path = args[1]
        print('HandlerDeleteDir is started. user: {} directory: {}'.format(alias, path))
        user = sql.User.query.filter_by(alias=str(alias)).first()
        if not user:
            return 'Wrong request parameters', 400
        port = user.port
        client_request = 'rmdir/{}/{}'.format(alias, path)
        answer = create_handler('request').run(alias, client_request, port)
        s = '/{}/{}%'.format(alias, path)
        if answer == 200:
            for f in sql.db.session.query(sql.File).filter(sql.File.name.like(s)).all():
                if f.owner == user:
                    sql.db.session.delete(f)
            sql.db.session.commit()
            return 'Success', 200
        else:
            return 'Wrong request parameters', 401


class HandlerInit(Handler):
    def __init__(self):
        super(HandlerInit, self).__init__()

    def run(self, *args):
        print('HandlerInit is started. user: {} '.format(args[0]))
        alias = args[0]
        user = sql.User.query.filter_by(alias=str(alias)).first()
        if not user:
            return 'Wrong request parameters', 400
        port = user.port
        answer = create_handler('request').run(alias, 'init/' + user.alias, port)
        if answer == 200:
            for f in sql.File.query.all():
                if f.owner == user:
                    sql.db.session.delete(f)
            sql.db.session.commit()
            return 'Success', 200
        else:
            return 'Wrong request parameters', 400


class HandlerRequest(Handler):
    def __init__(self):
        super(HandlerRequest, self).__init__()

    def run(self, *args):
        alias = args[0]
        command = args[1]
        port = args[2]
        print('HandlerRequest is started. user: {} command {}'.format(alias, command))
        servers = sql.User.query.filter_by(alias=str(alias)).first().tenant
        main_server = '{}:{}'.format(servers.mains.address, port)
        slave_server_1 = '{}:{}'.format(servers.seconds1.address, port)
        slave_server_2 = '{}:{}'.format(servers.seconds2.address, port)
        r = self.request_post(alias, command, main_server)
        # TODO: change returning values to requests, not requests code
        if r.status_code == 200:
            return 200
        elif self.request_post(alias, command, slave_server_1).status_code == 200:
            return 200
        elif self.request_post(alias, command, slave_server_2).status_code == 200:
            return 200
        else:
            return r.status_code

    def request_post(self, *args):
        alias = args[0]
        command = args[1]
        address = args[2]
        r = requests.post('http://{}/{}'.format(address, command), data={})
        # TODO: catch exceptions: unable to connect, etc.
        return r




def create_handler(type):
    handlers = {'login': HandlerLogin(), 'logout': HandlerLogout(),
                'read': HandlerRead(), 'write': HandlerWrite(), 'delete': HandlerDelete(),
                'size': HandlerSize(), 'mkdir': HandlerMkDir(), 'rmdir': HandlerRmDir(),
                'init': HandlerInit(), 'request': HandlerRequest(), 'register': HandlerRegister()
                }

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')
