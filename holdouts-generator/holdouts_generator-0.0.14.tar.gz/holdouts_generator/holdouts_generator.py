import os
import pickle
import shutil
import json
from auto_tqdm import tqdm
from typing import List, Callable
from .utils import get_level_description, cached, uncached, get_holdout_key

def _holdouts_generator(*dataset: List, holdouts: List, cacher:Callable, cache_dir:str=None, skip:Callable[[str], bool]=None, level: int = 0):
    if holdouts is None:
        return None

    def generator():
        for number, (outer, parameters, inner) in tqdm(enumerate(list(holdouts)), desc=get_level_description(level)):
            key = get_holdout_key(cache_dir, **parameters, level=level, number=number)
            if skip is not None and key is not None and skip(key):
                continue
            data = cacher(outer, dataset, cache_dir, **parameters, level=level, number=number)
            yield data, _holdouts_generator(
                *data[0],
                holdouts=inner,
                cacher=cacher,
                cache_dir=cache_dir,
                skip=skip,
                level=level+1
            )
    return generator

def holdouts_generator(*dataset: List, holdouts: List):
    """Return validation dataset and another holdout generator
        dataset, iterable of datasets to generate holdouts from.
        holdouts:List, list of holdouts callbacks.
    """
    return _holdouts_generator(*dataset, holdouts=holdouts, cacher=uncached)

def cached_holdouts_generator(*dataset: List, holdouts: List, cache_dir:str=".holdouts", skip:Callable[[str], bool]=None):
    """Return validation dataset and another holdout generator
        dataset, iterable of datasets to generate holdouts from.
        holdouts:List, list of holdouts callbacks.
        cache_dir:str=".holdouts", the holdouts cache directory.
        skip:Callable[str, bool], the callback for choosing to load or not a given holdout.
    """
    os.makedirs(cache_dir, exist_ok=True)
    return _holdouts_generator(*dataset, holdouts=holdouts, cacher=cached, cache_dir=cache_dir, skip=skip)

def clear_cache(cache_dir: str = ".holdouts"):
    """Remove the holdouts cache directory.
        cache_dir:str=".holdouts", the holdouts cache directory to be removed.
    """
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
