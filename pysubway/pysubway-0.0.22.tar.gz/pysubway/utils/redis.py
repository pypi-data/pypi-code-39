import redis


class Redis:
    def __init__(self, redis_url: str):
        self.r = redis.from_url(redis_url)

    def set(self, name, value, expired_time=None):
        """
        设置redis键值对
        :param name: 键名
        :param value: 值
        :param expired_time: 有效期
        """
        return self.r.set(name, value, expired_time)

    def get(self, name):
        """
        获取redis键值对
        :param name: 键名
        """
        return self.r.get(name)

    def ttl(self, name):
        """
        获取redis有效期
        :param name: 键名
        :return: 有效期
        """
        return self.r.ttl(name)

    def delete(self, *name):
        """
        删除redis键值对
        :param name: 键名
        """
        return self.r.delete(*name)
