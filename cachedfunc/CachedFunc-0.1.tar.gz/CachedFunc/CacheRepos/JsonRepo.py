import json
import time
from copy import deepcopy

from CachedFunc.CacheRepos.BaseCacheRepo import BaseCacheRepo


class JsonRepo(BaseCacheRepo):
    def __init__(self, filename, save_gap=5 * 60):
        self.filename = filename
        try:
            with open(filename) as f:
                self.storage = json.load(f)
        except FileNotFoundError:
            self.storage = {}
        self.save_gap = save_gap
        self.last_save = time.time()

    def __del__(self):
        with open(self.filename, 'w') as of:
            json.dump(self.storage, of)

    def get(self, key):
        return deepcopy(self.storage.get(key, None))

    def save(self, key, content):
        self.storage[key] = deepcopy(content)
        now = time.time()
        if now - self.last_save > self.save_gap:
            with open(self.filename, 'w') as of:
                json.dump(self.storage, of)
            self.last_save = now
        return True

    def has_key(self, key):
        return key in self.storage
