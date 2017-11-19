
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
        print('HandlerRead is started. file {}'.format(args[0]))
        return ''


class HandlerWrite(Handler):
    def __init__(self):
        super(HandlerWrite, self).__init__()

    def run(self, *args):
        print('HandlerWrite is started. file {}'.format(args[0]))
        return ''


class HandlerDelete(Handler):
    def __init__(self):
        super(HandlerDelete, self).__init__()
        pass

    def run(self, *args):
        print('HandlerDelete is started. file {}'.format(args[0]))
        return ''


class HandlerSize(Handler):
    def __init__(self):
        super(HandlerSize, self).__init__()

    def run(self, *args):
        print('HandlerSize is started. file {}'.format(args[0]))
        return ''


class HandlerMkDir(Handler):
    def __init__(self):
        super(HandlerMkDir, self).__init__()

    def run(self, *args):
        print('HandlerMkDir is started. file {}'.format(args[0]))
        return ''


class HandlerRmDir(Handler):
    def __init__(self):
        super(HandlerRmDir, self).__init__()

    def run(self, *args):
        print('HandlerRmDir is started. file {}'.format(args[0]))
        return ''


def create_handler(type):
    handlers = {'login': HandlerLogin(), 'logout': HandlerLogout(),
        'read': HandlerRead(), 'write': HandlerWrite(), 'delete': HandlerDelete(),
        'size': HandlerSize(), 'mkdir': HandlerMkDir(), 'rmdir': HandlerRmDir()
    }

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')