from sql import *


class Handler:
    def __init__(self):
        pass

    def run(self, *args):
        pass


class HandlerLogin(Handler):
    def __init__(self):
        super(HandlerLogin, self).__init__()

    def run(self, *args):
        request = args[0]
        session = args[1]

        if request.form['password'] == '' and request.form['username'] == '':
            session['logged_in'] = True
        else:
            return 'Unauthorized', 401

        return 'authorized', 200


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
        user = User.query.filter_by(alias=str(user_name)).first()
        if not user:
            return 'Wrong request parameters', 400

        if not File.query.filter_by(name=str('/' + user_name +'/' + path)).first():
            return 'File not found', 404
        else:
            try:
                servers = user.tenant
                return '{ "servers" : [ "' + servers.mains.address + '", "' + servers.seconds1.address + '", "' + servers.seconds2.address + '" ] }'
            except:
                return 'Wrong request parameters', 400

        # return ''


class HandlerWrite(Handler):
    def __init__(self):
        super(HandlerWrite, self).__init__()

    def run(self, *args):
        print('HandlerWrite is started. user: {} file: {}'.format(args[0], args[1]))
        user = User.query.filter_by(alias=str(args[0])).first()
        if not user:
            return 'Wrong request parameters', 400
        try:
            servers = user.tenant
            return '{ "servers" : [ "' + servers.mains.address + '", "' + servers.seconds1.address + '", "' + servers.seconds2.address + '" ] }'
        except:
            return 'Wrong request parameters', 400


class HandlerDelete(Handler):
    def __init__(self):
        super(HandlerDelete, self).__init__()
        pass

    def run(self, *args):
        #TODO: нужно возвращать только Success/Fault
        print('HandlerDelete is started. user: {} file: {}'.format(args[0], args[1]))
        user = User.query.filter_by(alias=str(args[0])).first()
        if not user:
            return 'Wrong request parameters', 400
        if not File.query.filter_by(name=str('/' + args[0] + '/' + args[1])).first():
            return 'File not found', 404
        else:
            try:
                servers = user.tenant
                return '{ "servers" : [ "' + servers.mains.address + '", "' + servers.seconds1.address + '", "' + servers.seconds2.address + '" ] }'
            except:
                return 'Wrong request parameters', 400


class HandlerSize(Handler):
    def __init__(self):
        super(HandlerSize, self).__init__()

    def run(self, *args):
        print('HandlerDelete is started. user: {} file: {}'.format(args[0], args[1]))
        user = User.query.filter_by(alias=str(args[0])).first()
        if not user:
            return 'Wrong request parameters', 400
        file = File.query.filter_by(name=str('/' + args[0] + '/' + args[1])).first()
        if not file:
            return 'File not found', 404
        else:
            try:
                return '{ "size" : ' + str(file.size) + ' }'
            except:
                return 'Wrong request parameters', 400


class HandlerMkDir(Handler):
    def __init__(self):
        super(HandlerMkDir, self).__init__()

    def run(self, *args):
        print('HandlerMkDir is started. user: {} directory: {}'.format(args[0], args[1]))
        user = User.query.filter_by(alias=str(args[0])).first()
        if not user:
            return 'Wrong request parameters', 400
        try:
            servers = user.tenant
            return '{ "servers" : [ "' + servers.mains.address + '", "' + servers.seconds1.address + '", "' + servers.seconds2.address + '" ] }'
        except:
            return 'Wrong request parameters', 400


class HandlerRmDir(Handler):
    def __init__(self):
        super(HandlerRmDir, self).__init__()

    def run(self, *args):
        # TODO: нужно возвращать только Success/Fault
        print('HandlerDelete is started. user: {} directory: {}'.format(args[0], args[1]))
        user = User.query.filter_by(alias=str(args[0])).first()
        if not user:
            return 'Wrong request parameters', 400
        if not File.query.filter_by(name=str('/' + args[0] + '/' + args[1])).first():
            return 'Directory not found', 404
        else:
            try:
                servers = user.tenant
                return '{ "servers" : [ "' + servers.mains.address + '", "' + servers.seconds1.address + '", "' + servers.seconds2.address + '" ] }'
            except:
                return 'Wrong request parameters', 400


class HandlerInit(Handler):
    def __init__(self):
        super(HandlerInit, self).__init__()

    def run(self, *args):
        # TODO: нужно возвращать только Success/Fault
        print('HandlerInit is started. user: {} '.format(args[0]))
        user = User.query.filter_by(alias=str(args[0])).first()
        if not user:
            return 'Wrong request parameters', 400
        try:
            servers = user.tenant
            return '{ "servers" : [ "' + servers.mains.address + '", "' + servers.seconds1.address + '", "' + servers.seconds2.address + '" ] }'
        except:
            return 'Wrong request parameters', 400


def create_handler(type):
    handlers = {'login': HandlerLogin(), 'logout': HandlerLogout(),
                'read': HandlerRead(), 'write': HandlerWrite(), 'delete': HandlerDelete(),
                'size': HandlerSize(), 'mkdir': HandlerMkDir(), 'rmdir': HandlerRmDir(),
                'init': HandlerInit()
                }

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')
