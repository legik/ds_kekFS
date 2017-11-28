import requests
import asyncio
import json
import os
import shutil
from filelock import FileLock
from config import NAMESERVER_1

LAST_UPDATE_FILE = 'storage/files/{0}_last_update'
UPDATES_FILE = 'storage/files/{0}_update.log'
LOCK = 'storage/files/{0}_filelock'
#RENAMES_FILE = 'storage/files/{0}_renames'


def log_update(user, path, operation, new_name=None):
    lock = FileLock(LOCK.format(user))
    with lock:
        with open(LAST_UPDATE_FILE.format(user), 'r') as f:
            last_update_id = int(f.read())
        with open(UPDATES_FILE.format(user), 'a+') as f:
            new_update = {'id': last_update_id + 1, 'operation': operation, 'path': path}
            if new_name is not None:
                new_update['new_name'] = new_name
            f.write(json.dumps(new_update) + '\n')
        with open(LAST_UPDATE_FILE.format(user), 'w') as f:
            f.write(str(last_update_id + 1))
    return


def get_full_path(user, path):
    return 'storage/files/{0}/{1}'.format(user, path)


def mkdir(user, path):
    full_path = get_full_path(user, path)
    try:
        os.mkdir(full_path, 0o775)
        log_update(user, path, 'mkdir')
    except FileExistsError:
        return False
    return True


def rmdir(user, path):
    full_path = get_full_path(user, path)
    try:
        shutil.rmtree(full_path)
        log_update(user, path, 'rmdir')
    except:
        return False
    return True


def delete(user, path):
    full_path = get_full_path(user, path)
    try:
        os.remove(full_path)
        log_update(user, path, 'delete')
    except:
        return False
    return True


def rename(user, path, new_name):
    new_path = path[:path.rfind('/') +1] + new_name
    full_path = get_full_path(user, path)
    new_full_path = get_full_path(user, new_path)
    if os.path.isfile(new_full_path) or os.path.isdir(new_full_path):
        return False
    try:
        shutil.move(full_path, new_full_path)
        #
        #     os.symlink(new_full_path, full_path)
        # else:
        #     lock = FileLock(LOCK.format(user))
        #     with lock:
        #         with open(RENAMES_FILE.format(user), 'r') as f:
        #             renames = json.loads(f.read())
        #         renames[path] = new_path
        #         with open(RENAMES_FILE.format(user), 'w') as f:
        #             f.write(json.dumps(renames))
        if os.path.isdir(new_full_path):
            log_update(user, path, 'rename_dir', new_path)
        else:
            log_update(user, path, 'rename_file', new_path)
    except:
        return False
    return True


def ask_nameserver(size, path, user):
    r = requests.get('http://{0}/submitted/{1}/{2}/{3}'.format(NAMESERVER_1, size, user, path))
    if r.status_code == 200:
        return r.json()
    else:
        return {'status': 'request failed'}


async def write_replica(address, port, path, temp_path):
    f = {'file': open(temp_path,'rb')}
    requests.post('http://{0}:{1}/write/{2}'.format(address, port, path), files=f)


async def async_replicate(replica_list, port, path, temp_path):
    loop = asyncio.get_event_loop()
    tasks = []
    for item in replica_list:
        task = loop.create_task(write_replica(item, port, path, temp_path))
        tasks.append(task)
    await tasks[0]


def replicate(replica_list, port, path, temp_path):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_replicate(replica_list, port, path, temp_path))
    except:
        pass
    return True


def rename_on_exist(user, path):
    path = get_full_path(user, path)
    i = 0
    new_path = path
    while os.path.isfile(new_path):
        i += 1
        x = path.rfind('.')
        new_path = path[:x] + '_' + str(i) + path[x:]
    return new_path


def get_data_version(user):
    lock = FileLock(LOCK.format(user))
    with lock:
        with open(LAST_UPDATE_FILE.format(user), 'r') as f:
            try:
                last_update = int(f.read())
            except:
                return 0
    return last_update


def get_update_list(user, version):
    lock = FileLock(LOCK.format(user))
    with lock:
        with open(UPDATES_FILE.format(user), 'r') as f:
            update_list = []
            for line in f:
                try:
                    update = json.loads(line)
                except:
                    return update_list
                if update['id'] > version:
                    update_list.append(update)
    return update_list


# def new_path_if_renamed(user, path):
#     new_path = path
#     lock = FileLock(LOCK.format(user))
#     with lock:
#         with open(RENAMES_FILE.format(user), 'r') as f:
#             renames = json.loads(f.read())
#     while renames[new_path] in renames:
#         new_path = renames[new_path]
#     return new_path

