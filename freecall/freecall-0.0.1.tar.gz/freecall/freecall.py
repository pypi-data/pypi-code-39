import functools
import json
import logging
import shelve
import zlib
import dill


def parameterize_deco(deco_to_replace):
    def deco_replacement(*args, **kwargs):
        def func_replacement(func_to_replace):
            return deco_to_replace(func_to_replace, *args, **kwargs)
        return func_replacement
    return deco_replacement


@parameterize_deco
def cache(func, force_hot=False, history_limit=5):
    @functools.wraps(func)
    def memo_wrapper(force_hot_, history_limit_, *args, **kwargs):
        func_name = func.__name__
        shelf = shelve.open("freecall.shelf")
        if "__meta" not in shelf:
            call_histories = {}
        else:
            call_histories = shelf["__meta_history"]  # [freecall.shelf][O][0]

        if func_name not in call_histories:
            call_histories[func_name] = []

        call_history = call_histories[func]

        try:
            call_hash = zlib.adler32(json.dumps((func, (args, kwargs)), default=dill.dumps, sort_keys=True).encode('utf-8')) & 0xffffffff
            hot = force_hot_ or call_hash not in call_history
        except dill.PicklingError as err:
            logging.warning(f"Calling cached function {func.__name__} with invalid arguments. Pickle error: \n {err}")
            hot = True
            call_hash = None

        if hot:
            func_result = func(*args, **kwargs)
            if call_hash is not None:
                call_history.append(func_result)
                if len(call_history) > history_limit:
                    for call_to_forget in call_history[:len(call_history) - history_limit]:
                        del shelf[call_to_forget]
                    call_history = call_history[-history_limit_:]
                shelf[call_hash] = func_result
                call_histories[func_name] = call_history

        else:
            func_result = shelf[call_hash]

        shelf["__meta_history"] = call_histories  # [freecall.shelf][0][C]
        shelf.close()
        return func_result

    return functools.partial(memo_wrapper, force_hot_=force_hot, history_limit_=history_limit)
