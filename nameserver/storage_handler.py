
from time import time
from time import sleep
import json
from threading import Lock
from threading import Timer
from db import sql
import requests

MAX_SIZE = 2 * 1024 * 1024 * 1024

def make_update_files_request(server):
    cluster_id = int((server.id - 1) / 3) + 1
    main_server = sql.Cluster.query.filter_by(id=str(cluster_id)).first().mains

    if server.address == main_server.address:
        server.updated = True
        sql.db.session.commit()
        return

    url = 'http://{0}:8010/uneedupdate/{1}'.format(server.address, main_server.address)
    r = requests.post(url)

    print('Send uneedupdate to {}'.format(server.address))

    if r.text == 'Updated\n':
        server.updated = True
        sql.db.session.commit()

    return

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
        self.delta = 7

    def run(self, *args):
        serv_addr = args[0]
        with self.mutex:
            self.servers_alive[serv_addr] = int(time())
        self.check_life_server()

        return '', 200

    def check_life_server(self):
        with self.mutex:
            serv_stat = self.servers_alive.copy()

        current_time = int(time())
        print('Current time: {}'.format(current_time))

        servers = sql.Server.query.all()
        for server in servers:
            addr = server.address
            if addr in serv_stat:
                if current_time - serv_stat[addr] > self.delta:
                    print('server-{0} rip. {1} - {2}'.format(addr, current_time, serv_stat[addr]))
                    HandlerAlive.swap_prime_server(server)
                else:
                    if server.status is True:
                        continue

                    print('server-{} now active'.format(addr))
                    if server.updated is False:
                        make_update_files_request(server)

                    server.status = True
                    sql.db.session.commit()
            else:
                #print('server-{} rip'.format(addr))
                HandlerAlive.swap_prime_server(server)

        #Timer(self.delta, self.check_life_server).start()

    @staticmethod
    def swap_prime_server(server):
        cluster_id = int((server.id - 1) / 3) + 1
        cluster = sql.Cluster.query.filter_by(id=str(cluster_id)).first()
        main_server = sql.Cluster.query.filter_by(id=str(cluster_id)).first().mains
        slave1 = sql.Cluster.query.filter_by(id=str(cluster_id)).first().seconds1
        slave2 = sql.Cluster.query.filter_by(id=str(cluster_id)).first().seconds2

        server.status = False
        server.updated = False
        sql.db.session.commit()

        is_main_server = (main_server.address == server.address)
        if is_main_server is not True:
            return

        if slave2.status is True and slave2.updated is True :
            tmp = main_server.id
            cluster.main = slave2.id
            cluster.second2 = tmp
            print('Switch to slave2')
        elif slave1.status is True and slave1.updated is True:
            tmp = main_server.id
            cluster.main = slave1.id
            cluster.second1 = tmp
            print('Switch to slave2')
        else:
            print('You are in a world of shit. No valid storage server available')

        sql.db.session.commit()


class HandlerSubmitted(Handler):
    def __init__(self):
        super(HandlerSubmitted, self).__init__()

    def run(self, *args):
        print('HandlerSubmitted is started.')

        size = int(args[0])
        path = args[1]
        addr = args[2]

        server_id = sql.Server.query.filter_by(address=addr).first().id
        cluster_id = int((server_id - 1) / 3) + 1
        cluster = sql.Cluster.query.filter_by(id=str(cluster_id)).first()

        if cluster.mains.address != addr:
            return json.dumps({'status': 'not allowed - not prime serv'}), 200

        user_name = path.split('/')[0]
        user_id = sql.User.query.filter_by(alias=user_name).first().id
        print(user_id)

        if HandlerSubmitted.check_availbel_size(user_name, size) is False:
            return json.dumps({'status': 'not allowed - size'}), 200

        if sql.File.query.filter_by(name='/'+path).first() is not None:
            return json.dumps({'status': 'not allowed - exists'}), 200

        file = sql.File(name='/'+path, size=size, user_id=user_id)
        sql.db.session.add(file)
        sql.db.session.commit()

        HandlerSubmitted.updated_size(user_name, size)

        slave1 = sql.Cluster.query.filter_by(id=str(cluster_id)).first().seconds1
        slave2 = sql.Cluster.query.filter_by(id=str(cluster_id)).first().seconds2

        replica_list = []

        if slave1.status is True:
            replica_list.append(slave1.address)

        if slave2.status is True:
            replica_list.append(slave2.address)

        return json.dumps({'status': 'allowed', 'replicas': replica_list}), 200

    @staticmethod
    def check_availbel_size(user_name, size):
        available_size = sql.User.query.filter_by(alias=user_name).first().size
        return int(available_size) + size <= MAX_SIZE

    @staticmethod
    def updated_size(user_name, size):
        user = sql.User.query.filter_by(alias=user_name).first()
        user.size = str(int(user.size) + size)
        sql.db.session.commit()


class HandlerUpdated(Handler):
    def __init__(self):
        super(HandlerUpdated, self).__init__()

    def run(self, *args):
        print('HandlerUpdated is started.')

        server_adr = args[0]
        server = sql.Server.query.filter_by(address=server_adr).first()

        server.updated = True
        sql.db.session.commit()

        return '', 200


class HandlerUpdatedFailed(Handler):
    def __init__(self):
        super(HandlerUpdatedFailed, self).__init__()

    def run(self, *args):
        print('HandlerUpdated is started.')

        server_addr = args[0]

        sleep(10)

        server = sql.Server.query.filter_by(address=server_addr).first()
        make_update_files_request(server)

        return '', 200


class HandlerRemoveUser(Handler):
    def __init__(self):
        super(HandlerRemoveUser, self).__init__()

    def run(self, *args):
        print('HandlerUpdated is started.')

        user_name = args[0]

        user = sql.User.query.filter_by(alias=user_name).first()
        if user is None:
            return 'User not found', 200

        cluster = sql.Cluster.query.filter_by(id=user.cluster).first()

        while True:
            file = sql.File.query.filter_by(user_id=user.id).first()
            if file is None:
                break
            sql.db.session.delete(file)


        sql.db.session.delete(user)
        sql.db.session.commit()

        servers = [cluster.mains, cluster.second1, cluster.second2]
        for serv in servers:
            try:
                url = '{0}:8010/kill/{1}'.format(serv.address, user_name)
                requests.post(url)
            except:
                pass

        return '', 200


handlerAlive = HandlerAlive()


def create_handler(type):
    global handlerAlive
    handlers = {'alive': handlerAlive, 'submitted': HandlerSubmitted(),
                'updated': HandlerUpdated(), 'updated_failed': HandlerUpdatedFailed(),
                'remove_user': HandlerRemoveUser()}

    if type in handlers.keys():
        return handlers[type]
    else:
        raise Exception('Unknown Handler')