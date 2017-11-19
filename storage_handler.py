
class Handler:
    def __init__(self):
        pass

    def run(self, *args):
        pass


class HandlerAlive(Handler):
    def __init__(self):
        super(HandlerAlive, self).__init__()

    def run(self, *args):
        print('HandlerAlive is started.')
        return ''


def create_handler(type):
    handlers = {'alive': HandlerAlive()
    }

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')