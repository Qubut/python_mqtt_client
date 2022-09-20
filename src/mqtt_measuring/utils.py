from glob import glob
import logging
import os.path
import asyncio
from hashlib import md5
from json import dumps, loads


def get_size(fpath):
    return int(os.path.getsize(fpath)/1024)


def dump_json(msg): return dumps(msg)
def load_json(msg): return loads(msg)
def chunk_md5(chunk): return md5(chunk).hexdigest()


def check_file(f):
    return os.path.isfile(f)


def check_path(path): return os.path.exists(path)


def mk_dir(dir): return os.makedirs(dir)


def exit(err):
    os._exit(err)
    os.kill(os.getpid)


def generate_md5(fname):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_temp_files(od, filename, timeid, filehash):
    """ check temp file and rename to original
    """
    os.sync()
    for l in os.listdir(od):
        nameid = l.split("_")[0]
        if nameid == timeid:
            if generate_md5(od+"/"+l) == filehash:
                os.rename(od+"/"+l, od+"/"+filename)
    for f in glob(od+"/*.temp"):
        os.remove(f)
    logging.info("OK: saved file", filename)
