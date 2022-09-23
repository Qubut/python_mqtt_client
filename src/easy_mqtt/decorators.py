from types import FunctionType
from time import time
from typing import Any

def timed(f):
    def wrap(*args, **kargs)->tuple[Any,float]:
        t0 = time()
        result:Any = f(*args,**kargs)
        t = time()
        elapsed = (t - t0)
        return result, elapsed if elapsed < 1 else elapsed
    return wrap
