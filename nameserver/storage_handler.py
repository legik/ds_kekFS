
from time import time
from threading import Lock
from threading import Timer
from db import sql

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
        self.delta = 5
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
        serv_stat = self.servers_alive
        self.mutex.release()

        current_time = int(time())

        print('Check value: {}'.format(current_time))

        servers = sql.Server.query.all()
        for server in servers:
            addr = server.address
            if addr in serv_stat:
                if current_time - serv_stat[addr] > self.delta:
                    print('server-{} rip'.format(addr))
                    HandlerAlive.swap_prime_server(server)
                else:
                    print('server-{} active'.format(addr))
                    server.status = True
            else:
                print('server-{} rip'.format(addr))
                HandlerAlive.swap_prime_server(server)

        Timer(self.delta, self.check_life_server).start()

    @staticmethod
    def swap_prime_server(server):
        cluster_id = int((server.id - 1) / 3) + 1
        main_server = sql.Cluster.query.filter_by(id=str(cluster_id)).first().mains
        slave1 = sql.Cluster.query.filter_by(id=str(cluster_id)).first().seconds1
        slave2 = sql.Cluster.query.filter_by(id=str(cluster_id)).first().seconds2

        server.status = False
        sql.db.session.commit()

        is_main_server = (main_server.address == server.address)
        if is_main_server is not True:
            return

        if slave2.status is True:
            tmp = main_server
            main_server = slave2
            slave2 = tmp
        elif slave1.status is True:
            tmp = main_server
            main_server = slave1
            slave1 = tmp
        else:
            print('You are in a world of shit. No valid storage server available')

        sql.db.session.commit()


class HandlerSubmitted(Handler):
    def __init__(self):
        super(HandlerSubmitted, self).__init__()

    def run(self, *args):
        print('HandlerSubmitted is started.')

        size = args[0]
        path = args[1]

        user_name = path.split('/')[0]
        user_id = sql.User.query.filter_by(alias=user_name).first().id
        print(user_id)

        file = sql.File(name=path, size=size, user_id=user_id)
        sql.db.session.add(file)
        sql.db.session.commit()

        return '', 200


handlerAlive = HandlerAlive()


def create_handler(type):
    global handlerAlive
    handlers = {'alive': handlerAlive, 'submitted': HandlerSubmitted()}

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')