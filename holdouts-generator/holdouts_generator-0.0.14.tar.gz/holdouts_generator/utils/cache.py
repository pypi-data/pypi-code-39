from typing import Callable, List, Dict
from .paths import pickle_path, info_path
from .various import odd_even_split
from .hash import hash_file
import os
import pandas as pd
import pickle


def uncached(generator: Callable, dataset: List, *args, **kwargs):
    return odd_even_split(generator(dataset))


def cached(generator: Callable, dataset: List, cache_dir: str, **parameters: Dict):
    path = pickle_path(cache_dir, **parameters)
    try:
        return load(path)
    except (pickle.PickleError, FileNotFoundError):
        data = odd_even_split(generator(dataset))
    key = dump(data, cache_dir, path, **parameters)
    return (*data, key)


def load(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


def build_info(path: str, parameters: Dict, key: str)->pd.DataFrame:
    return pd.DataFrame({
        "path": path,
        "key": key,
        **parameters
    }, index=[0])


def dump(data, cache_dir: str, path: str, **parameters: Dict)->str:
    with open(path, "wb") as f:
        pickle.dump(data, f)
    key = hash_file(path)
    info_file = info_path(cache_dir)
    info = build_info(path, parameters, key)
    if os.path.exists(info_file):
        info = pd.concat([pd.read_csv(info_file), info])
    info.to_csv(info_file, index=False)
    return key


def get_holdout_key(cache_dir: str, **parameters: Dict)->str:
    """Return key, if cached, for given holdout.
        cache_dir:str, cache directory to load data from
        parameters:Dict, parameters used to generated the holdout.
    """
    try:
        return pd.read_csv(info_path(cache_dir)).query(" & ".join([
            "{key} == {value}".format(key=key, value=value)
            for key, value in parameters.items()
        ]))["key"].values[0]
    except (FileNotFoundError, IndexError):
        pass
