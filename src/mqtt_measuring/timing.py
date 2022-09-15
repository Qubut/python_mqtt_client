
from types import FunctionType
from time import time

def timed(f):
    def wrap(*args, **kargs):
        t0 = time.time()
        result = f(*args,**kargs)
        t = time.time()
        elapsed = t - t0
        return result, elapsed
    return wrap

