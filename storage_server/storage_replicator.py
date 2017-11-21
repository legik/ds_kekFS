from flask import Flask
import json
import filelock
import requests
import storage_writes

PORT = os.environ['SSC_PORT']
USERNAME = os.environ['SSC_USERNAME']

@app.route('/delete/<path:path>', methods=['POST'])
def delete(path):
	if '../' in path:
		return 'Forbidden path\n'
	full_path = 'files/{0}'.format(path)
	try:
		os.remove(full_path)
	except:
		return 'File does not exist\n'
	return 'Success\n'

@app.route('/rmdir/<path:path>', methods=['POST'])
def rmdir(path):
	if '../' in path:
		return 'Forbidden path\n'
	full_path = 'files/{0}'.format( path)
	try:
		shutil.rmtree(full_path)
	except:
		return 'Directory does not exist\n'
	return 'Success\n'

@app.route('/getupdate/<address>', methods=['POST'])
def update(address):
	r = requests.post('http://giveupdate/{0}'.format(storage_writes.get_data_version()))
	return 

@app.route('/uneedupdate/<address>/', methods=['POST'])

@app.route('/giveupdate/<int:updateid>'. methods=['POST'])
def giveupdate(updateid):

	if username in provider_pool:
		provider_pool[username].terminate()
	new_env = os.environ.copy()
	new_env['FLASK_APP'] = 'storage_provider.py'
	new_env['SSC_PORT'] = str(port)
	new_env['SSC_USERNAME'] = str(username)
	provider_pool[username] = Popen(['python','updater.py', str(port), str(path)])
	
	return

