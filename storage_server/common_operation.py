
import os
import shutil


def command_mkdir(path):
    full_path = format_full_path(path)
    try:
        os.mkdir(full_path, 0o553)
    except FileExistsError:
        return False
    return True


def command_rmdir(path):
    full_path = format_full_path(path)
    try:
        shutil.rmtree(full_path)
    except:
        return False
    return True


def command_delete(path):
    full_path = format_full_path(path)
    try:
        os.remove(full_path)
    except:
        return False
    return True


def format_full_path(path):
    return 'files/{0}'.format(path)