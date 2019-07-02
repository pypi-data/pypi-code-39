import functools
import json
import logging
import shelve
import sys
import zlib
import dill


def parameterize_deco(deco_to_replace):
    def deco_replacement(*args, **kwargs):
        def func_replacement(func_to_replace):
            return deco_to_replace(func_to_replace, *args, **kwargs)

        return func_replacement

    return deco_replacement


def checksum_dump(obj: object):
    return zlib.adler32(dill.dumps(obj))


@parameterize_deco
def cache(func, force_hot=False, history_limit=5):
    @functools.wraps(func)
    def memo_wrapper(*args, force_hot_, history_limit_, **kwargs, ):
        None if not force_hot_ else logging.debug(f"Calling [{func.__name__}] forcibly hot")
        func_name = func.__name__
        shelf = shelve.open("freecall.shelf")

        if "__meta_history" not in shelf:
            call_histories = {}
        else:
            call_histories = shelf["__meta_history"]  # [freecall.shelf][O][0]
        if func_name not in call_histories:
            call_histories[func_name] = []

        try:
            call_parts = (func, args, kwargs)
            call_hash = str(zlib.adler32(json.dumps(call_parts, default=checksum_dump, sort_keys=True).encode('utf-8')) & 0xffffffff)
            logging.debug(f"Call hash successfully computed: {call_hash}")
            hot = force_hot_ or call_hash not in call_histories[func_name]
        except dill.PicklingError as err:
            logging.warning(f"Calling cached function {func.__name__} with invalid arguments. Defaulting to HOT. Pickle error: \n {err}")
            hot = True
            call_hash = None

        if hot:
            call_history = call_histories[func_name]
            logging.debug(f"Function {func.__name__} hot, calling function")
            func_result = func(*args, **kwargs)
            if call_hash is not None and call_hash not in call_history:
                call_history.append(call_hash)
                if len(call_history) > history_limit:
                    for call_to_forget in call_history[:len(call_history) - history_limit]:
                        del shelf[call_to_forget]
                    call_history = call_history[-history_limit_:]
                shelf[call_hash] = func_result
                call_histories[func_name] = call_history
                logging.debug(f"Call history: {call_history}")

        else:
            logging.debug(f"Function {func.__name__} already saved, loading")
            func_result = shelf[call_hash]

        shelf["__meta_history"] = call_histories  # [freecall.shelf][0][C]
        shelf.close()
        return func_result

    return functools.partial(memo_wrapper, force_hot_=force_hot, history_limit_=history_limit)


def heat(func: callable):
    """Convenience method that """
    return functools.partial(func, force_hot_=True)
