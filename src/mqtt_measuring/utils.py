import base64
from glob import glob
import os.path
from hashlib import md5
from json import dumps, loads
import logging
import sys
"""
This is a module containing 
the functions used by both publish.py and subscribe.py
    
"""


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s", handlers=[
                        logging.FileHandler('./out/log.log'),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger(__name__)


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


def make_temp(od: str, data: bytes, hash: str, number: int, timeid: int, filename: str):
    """ save data to temp file
        and send recieved chunknumber
    """
    if chunk_md5(data.encode()) == hash:
        fname = od+"/"+str(timeid)+"_"+filename+"_.temp"
        with open(fname, "wb" if number == 0 else "ab") as f:
            try:
                f.write(base64.b64decode(data))
            except Exception as e:
                logger.error(e)
                return False
        logger.info(f"saved chunk {number} to {fname}")
        return True


def check_temp_files(od: str, filename: str, timeid: int, filehash: str):
    """ checks temp files and rename to original
    """
    os.sync()
    for l in os.listdir(od):
        nameid = l.split("_")[0]
        if nameid == timeid:
            if generate_md5(od+"/"+l) == filehash:
                os.rename(od+"/"+l, od+"/"+filename)
    for f in glob(od+"/*.temp"):
        os.remove(f)
    logging.info(f"OK: saved file {filename}")
