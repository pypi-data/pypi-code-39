"""Provide a decorator for measuring function execute time and memory usage."""
import time
from functools import wraps
from memory_profiler import memory_usage
from typing import Callable


def profile(time_prof: bool = True, mem_prof: bool = False) -> Callable:
    """Multilayered decorator for wrapping a func with arguments.
    
    time_prof - measure run time - default: True
    mem_prof - measure memory - default: False
    """

    def real_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            fn_kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            fn_args_str = ", ".join(f"{v}" for v in args)
            print(f"\n{fn.__name__}({fn_args_str}, {fn_kwargs_str})")

            if time_prof:
                t = time.perf_counter()
                retval = fn(*args, **kwargs)
                elapsed = time.perf_counter() - t
                print(f"Time   {elapsed:.8f}")

            if mem_prof:
                mem, retval = memory_usage(
                    (fn, args, kwargs), retval=True, timeout=200, interval=1e-7
                )

                print(f"Memory {max(mem) - min(mem)}")

            return retval

        return wrapper

    return real_decorator
