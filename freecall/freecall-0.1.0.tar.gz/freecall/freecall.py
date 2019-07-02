import functools
import json
import logging
import shelve
import sys
import zlib
import dill

__CACHE_NAME__ = "freecall.shelf"


def set_cache_file(new_cache_file: str) -> None:
    """
    Changes the storage location of the cache. Directly used by shelve.open, and hence has the same possible side-effects of extensions or multiple file creation.
    :param new_cache_file: The new filename for the cache.
    """
    global __CACHE_NAME__
    __CACHE_NAME__ = new_cache_file


def _parameterize_deco(deco_to_replace):
    def deco_replacement(*args, **kwargs):
        def func_replacement(func_to_replace):
            return deco_to_replace(func_to_replace, *args, **kwargs)
        return func_replacement
    return deco_replacement


def _checksum_dump(obj: object):
    return zlib.adler32(dill.dumps(obj))


@_parameterize_deco
def cache(func, force_hot: bool = False, history_limit: int = 5, disable_cache: bool = False) -> callable:
    """
    Automatically memoizes decorated functions to disk in freecall.shelf.
    :param func: Function to memoize.
    :param force_hot: Forces function to always recompute values.
    :param history_limit: Number of function calls to remember. If reduced from a previous run, will truncate history to match new limit.
    :param disable_cache: Disables the cache entirely for this function. Provided for convenience, will simply call the function and return the result.
    :return: Wrapped, memoizing function. Can be manually adjusted with force_hot_, history_limit_, and disable_cache_, corresponding to the decorator parameters.
    """

    @functools.wraps(func)
    def memo_wrapper(*args, force_hot_, history_limit_, disable_cache_=False, **kwargs, ) -> functools.partial:
        if disable_cache_:
            return func(*args, **kwargs)

        None if not force_hot_ else logging.debug(f"Calling [{func.__name__}] forcibly hot")
        func_name = func.__name__
        shelf = shelve.open("freecall.shelf")
        logging.debug("Loaded cache ")
        if "__meta_history" not in shelf:
            logging.info(f"First run, initializing shelf")
            call_histories = {}
        else:
            call_histories = shelf["__meta_history"]  # [freecall.shelf:__meta_history][0][R]
        if func_name not in call_histories:
            call_histories[func_name] = []

        try:
            call_parts = (func, args, kwargs)
            call_hash = str(zlib.adler32(json.dumps(call_parts, default=_checksum_dump, sort_keys=True).encode('utf-8')) & 0xffffffff)
            logging.debug(f"Call hash successfully computed: {call_hash}")
            hot = force_hot_ or call_hash not in call_histories[func_name]
        except dill.PicklingError as err:
            logging.warning(f"Calling cached function [{func_name}] with invalid arguments. Defaulting to HOT. Pickle error: \n {err}")
            hot = True
            call_hash = None

        if hot:
            call_history = call_histories[func_name]
            logging.debug(f"Function [{func_name}] hot, calling function")
            func_result = func(*args, **kwargs)
            if call_hash is not None and call_hash not in call_history:
                call_history.append(call_hash)
                # Forget old calls
                if len(call_history) > history_limit:
                    for call_to_forget in call_history[:-history_limit]:
                        del shelf[call_to_forget]
                    call_history = call_history[-history_limit_:]
                # Cache new call
                shelf[call_hash] = func_result
                call_histories[func_name] = call_history
                logging.debug(f"Saving call to [{func_name}] at call hash [{call_hash}]")

        else:
            logging.debug(f"Function [{func_name}] already saved with call hash {call_hash}, loading")
            func_result = shelf[call_hash]

        shelf["__meta_history"] = call_histories  # [freecall.shelf:__meta_history][0][W]
        shelf.close()
        return func_result

    return functools.partial(memo_wrapper, force_hot_=force_hot, history_limit_=history_limit, disable_cache_=disable_cache)


def heat(func: callable) -> functools.partial:
    """
    Convenience method that converts a @cache decorated function to one that always recomputes
    :param func: @cache decorated function
    :return: A @cache decorated function that will always recompute the value
    """
    return functools.partial(func, force_hot_=True)


def no_cache(func: callable) -> functools.partial:
    """
    Convenience method that converts a @cache decorated function into one that bypasses the cache entirely,
    without loading or saving to it.
    :param func: @cache decorated function
    :return: A @cache decorated function that will ignore the cache entirely
    """
    return functools.partial(func, disable_cache_=True)
