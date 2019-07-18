import inspect
import json
import logging
import uuid
from collections import OrderedDict
from functools import wraps

from CachedFunc.CacheRepos import MemRepo
from CachedFunc.CacheRepos.BaseCacheRepo import BaseCacheRepo
from CachedFunc.NotInCacheError import NotInCacheError


class CacheManager:
    def __init__(self):
        self.__repos = OrderedDict()

    def add_repo(self, repo, name=None):
        if not isinstance(repo, BaseCacheRepo):
            raise TypeError('Need an instance of BaseCacheRepo.')
        if name is None:
            name = uuid.uuid4()
        if name in self.__repos:
            raise ValueError('Duplicate repo name %s.', name)
        self.__repos[name] = repo
        return name

    def get_repo(self, name):
        if name not in self.__repos:
            raise NotInCacheError(name)
        return self.__repos[name]

    def get(self, key):
        if len(self.__repos) == 0:
            logging.warning('No repo in CacheManager')
        asked_repos = []
        for name, repo in self.__repos.items():
            if key in repo:
                return repo[key], asked_repos
            else:
                asked_repos.append(name)
        raise NotInCacheError(key)

    def register(self, func):
        def gen_key(*args, **kwargs):
            params = inspect.signature(func).parameters
            sig_dict = {}
            # assign parameters to corresponding slots
            end = 0
            for i, k in enumerate(params.values()):
                if k.kind.name == 'POSITIONAL_OR_KEYWORD':
                    if i < len(args):
                        end = i + 1
                        sig_dict[k.name] = args[i]
                    elif k.name in kwargs:
                        sig_dict[k.name] = kwargs[k.name]
                        del kwargs[k.name]
                    else:
                        if k.default is inspect._empty:
                            raise TypeError(f'{func.__name__}() missing 1 required positional argument: \'{k.name}\'')
                        sig_dict[k.name] = k.default
            args = args[end:]
            key = '|'.join([func.__name__, json.dumps(sig_dict), json.dumps(args), json.dumps(kwargs)])
            return key

        @wraps(func)
        def wrapper(*args, **kwargs):
            force_refresh = kwargs.get('_cached_func_force_refresh', False)
            if '_cached_func_force_refresh' in kwargs:
                del kwargs['_cached_func_force_refresh']
            key = gen_key(*args, **kwargs)
            if force_refresh:
                value = func(*args, **kwargs)
                update_needed = self.__repos.keys()
            else:
                try:
                    value, update_needed = self.get(key)
                except NotInCacheError:
                    value = func(*args, **kwargs)
                    update_needed = self.__repos.keys()
            # update downstream repos
            for name in update_needed:
                logging.debug(f'update {name} with value {value}')
                self.__repos[name][key] = value
            return value

        return wrapper
