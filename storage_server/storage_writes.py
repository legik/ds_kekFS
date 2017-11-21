import requests
import asyncio
import json
import config
from filelock import FileLock

UPDATES_FILE = 'update.log'
lock = FileLock(UPDATES_FILE)

def ask_nameserver(operation, path, user):
	r = requests.get('http://{0}/ask/{1}/{2}'.format(config.NAMESERVER, operation, path, filesize), data = {'user': user})
	return r.json()

def log_update(user, path, operation):
	lock.acquire()
	with open('files/{0}/{1}'.format(user, UPDATES_FILE), 'a+') as f:
		new_update = {}
		try:
			last_update = json.loads(f.readline())
		except:
			new_update['id'] = 1
		else:
			new_update['id'] = last_update['id'] + 1
		finally:
			new_update['operation'] = operation
			new_update['path'] = path_inc_user
			f.write(json.dumps(new_update) + '\n')
	lock.release()

def write_replica(address, path):
	f = {'upload_file': open(path,'rb')}
	r = requests.post('http://{0}'.format(address), files = f)
	return r.json()

def replicate(locations, path):
	try:
		loop = asyncio.get_event_loop()
		tasks = [] 
		for item in locations:
			task = asyncio.ensure_future(write_replica(item, path))
			tasks.append(task)
		loop.run_until_complete(asyncio.wait(tasks))
		loop.close()
	except:
		return False
	return True

def rename_on_exist(path):
	i = 0
	new_path = path
	while os.path.isfile(new_full_path):
		i += 1
		x = full_path.rfind('.')-1
		new_path = path[:x]+ '_' + str(i) + path[x:]
	return new_path

def get_data_version():
	lock.acquire()
	with open(UPDATES_FILE, 'r') as f:
		try:
			last_update = json.loads(f.readline())
		except:
			lock.release()
			return 0
	lock.release()
	return last_update['id']

def get_update_list(there_version):
	lock.acquire()
	with open(UPDATES_FILE, 'r') as f:
		try:
			last_update = json.loads(f.readline())
		except:
			lock.release()
			return []
		if last_update['id'] < there_version:

		if last_update['id'] > there_version:

		if last_update['id'] = there_version:
			lock.release()
			return []
	return 

def push_updates(version):
	there_version = version
	here_version = get_data_version()
	while there_version != here_version:
		lock.acquire()
		with open(UPDATES_FILE, 'r') as f:
			try:
			last_update = json.loads(f.readline())
	return
