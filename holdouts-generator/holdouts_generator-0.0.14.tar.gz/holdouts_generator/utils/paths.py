from dict_hash import sha256

def pickle_path(cache_directory: str, **parameters)->str:
    return "{cache_directory}/{hash}.pickle".format(
        cache_directory=cache_directory,
        hash=sha256(parameters)
    )

def info_path(cache_directory: str)->str:
    return "{cache_directory}/cache.csv".format(
        cache_directory=cache_directory
    )