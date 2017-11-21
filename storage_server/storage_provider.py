from flask import Flask, send_from_directory, request
import os
import shutil
import json
import storage_writes

app = Flask(__name__)

PORT = os.environ['SSC_PORT']
USERNAME = os.environ['SSC_USERNAME']

@app.route('/write/<path:path>', methods=['POST'])
def write(path):
	if '../' in path:
		return 'Forbidden path\n'
	if 'file' not in request.files:
		return 'File is not provided'
	f = request.files['file']
	if f.filename == '':
		return 'File is not provided'
	full_path = 'files/{0}'.format(path)
	pss = storage_writes.ask_nameserver(USERNAME, filesize)
	if 'status' not in pss or pss['status'] != 'allowed' or len(pss['replicas']) not in [1, 2]:
		return 'Operation is not allowed\n'
	full_path = storage_writes.rename_on_exist(full_path)
	try:
		f.save(full_path)
		log_update(operation, path_inc_user)
	except:
		return 'Directory does not exist\n'
	storage_writes.replicate(pss['replicas'])
	return 'Success\n'

@app.route('/read/<path:path>', methods=['GET'])
def read(path):
	if '../' in path:
		return 'Forbidden path\n'
	return send_from_directory('files/', path, as_attachment=True)

@app.route('/mkdir/<path:path>', methods=['POST'])
def mkdir(path):
	if '../' in path:
		return 'Forbidden path\n'
	full_path = 'files/{0}'.format(path)
	try:
		os.mkdir(full_path, 0o553)
	except FileExistsError:
		return 'Directory already exists\n'
	return 'Success\n'

@app.route('/lsdir/<path:path>', methods=['GET'])
def listdir(path):
	if '../' in path:
		return 'Forbidden path\n'
	full_path = 'files/{0}/{1}'.format(USERNAME, path)
	d = []
	try:
		ls = os.scandir(full_path)
		for item in ls:
			c = {}
			c['dir'] = item.is_dir()
			c['name'] = item.name
			d.append(c)
	except:
		return 'Directory does not exist\n'
	return json.dumps(d)

