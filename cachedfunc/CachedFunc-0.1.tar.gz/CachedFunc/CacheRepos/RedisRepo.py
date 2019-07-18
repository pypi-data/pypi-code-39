import redis
import pickle

from CachedFunc.CacheRepos.BaseCacheRepo import BaseCacheRepo


class RedisRepo(BaseCacheRepo):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host, port, db)

    def get(self, key):
        value = self.redis.get(key)
        if value is None:
            return None
        return pickle.loads(value)

    def save(self, key, content):
        self.redis.set(key, pickle.dumps(content))
        return True

    def has_key(self, key):
        return self.redis.exists(key)
