from glob import glob
import logging
import os.path
from hashlib import md5
from json import dumps, loads
from .logger import logger
"""
This is a module containing 
the functions used by both publish.py and subscribe.py
    
"""




def dump_json(msg: bytes) -> str:
    """calls the function json.dumps to serialize an object
    to a json formatted str

    Args:
        msg (bytes): the payload to be published by the MQTT client

    Returns:
        str: A json formatted string
    """
    return dumps(msg)


def load_json(msg: str) -> bytes:
    """calls the function json.loads to deserialize a json formatted string to an object

    Args:
        msg (str): the payload recieved from the publisher

    Returns:
        object: the deserialized object json fromatted payload
    """
    return loads(msg)


def chunk_md5(chunk: bytes) -> str:
    """returns the md5 hash of a chunk of bytes

    Args:
        chunk (bytes): the chunk of data to be hashed

    Returns:
        str: the md5 hash of the chunk of data
    """
    return md5(chunk).hexdigest()


def check_file(f: str) -> bool:
    """checks if a file exits in the path

    Args:
        f (str): the full or relative path of the file

    Returns:
        bool: the result of checking the file's existance
    """
    return os.path.isfile(f)


def check_path(path: str) -> bool:
    """checks if the given path is valid

    Args:
        path (str): the path to a directory in the OS

    Returns:
        bool: the result for the checking the path
    """
    return os.path.exists(path)
def get_size(fpath: str) -> int:
    """returns the size of the given file

    Args:
        fpath (str): the full or relative path of the file

    Returns:
        int: the size of the file in KB 
    """
    if check_file(fpath):
        return int(os.path.getsize(fpath)/1024)
    else:
        raise FileNotFoundError

def mk_dir(dir: str):
    """makes a dir in the given path

    Args:
        dir (str): the full or relative path to the directory

    Returns:
        None
    """
    if check_path(dir):
        logger.info(f"Directory {dir} already exits")
        return
    os.makedirs(dir)


def exit(err: int):

    os._exit(err)
    os.kill(os.getpid)


def generate_md5(fname) -> str:
    """generates the md5 hash of a given file

    Args:
        fname (str): full or relative path to the file

    Returns:
        str: the md5 hash of the file
    """
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_temp_files(od: str, filename: str, timeid: int, filehash: str):
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
