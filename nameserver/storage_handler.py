
from time import time
from threading import Lock
from threading import Timer


class Handler:
    def __init__(self):
        pass

    def run(self, *args):
        pass


class HandlerAlive(Handler):
    def __init__(self):
        super(HandlerAlive, self).__init__()
        self.servers_alive = {}
        self.mutex = Lock()
        self.check_life_server()

    def run(self, *args):
        print('HandlerAlive is started.')
        serv_addr = args[0]

        self.mutex.acquire()
        self.servers_alive[serv_addr] = int(time())
        self.mutex.release()

        return '', 200

    def check_life_server(self):
        self.mutex.acquire()
        servers = self.servers_alive
        self.mutex.release()

        current_time = int(time())
        delta = 10

        print('Check value: {}'.format(current_time))

        for addr, serv_time in servers.items():
            if current_time - serv_time > delta:
                print('Dye')
            else:
                print('Alive')

        Timer(10, self.check_life_server).start()


handlerAlive = HandlerAlive()


def create_handler(type):
    global handlerAlive
    handlers = {'alive': handlerAlive}

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')