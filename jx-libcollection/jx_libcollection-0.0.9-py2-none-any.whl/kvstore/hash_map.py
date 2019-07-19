from lib_collection.kvstore.linked_list import LinkedListKVStore


class HashMap(object):

    __item_cnt_per_bucket__ = 10

    def __init__(self, bucket_cnt=3):
        self.bucket_cnt = bucket_cnt
        self.n = 0
        self.buckets = [LinkedListKVStore() for _ in range(self.bucket_cnt)]

    def __len__(self):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> len(d)
        1
        >>> d['b'] = 2
        >>> d['a'] = 3
        >>> len(d)
        2
        """
        return self.n

    def __setitem__(self, k, v):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> for i in range(40):
        ...     d[str(i)] = i
        ...
        >>> d.bucket_cnt
        7
        """
        if self.bucket_cnt * self.__item_cnt_per_bucket__ <= self.n:
            new_bucket_cnt = self.bucket_cnt * 2 + 1
            new_hash_map = HashMap(new_bucket_cnt)
            new_hash_map[k] = v
            for _k, _v in self:
                new_hash_map[_k] = _v
            self.bucket_cnt = new_hash_map.bucket_cnt
            self.n = new_hash_map.n
            self.buckets = new_hash_map.buckets
        else:
            h = self._hash(k)
            bucket = self.buckets[h]
            if k not in bucket:
                self.n += 1
            bucket[k] = v

    def __getitem__(self, k):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> d['a']
        1
        >>> d['b'] = 2
        >>> d['a'] = 3  # test update
        >>> d['a']
        3
        """
        h = self._hash(k)
        return self.buckets[h][k]

    def __contains__(self, k):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> 'a' in d
        True
        >>> 'b' in d
        False
        """
        h = self._hash(k)
        return k in self.buckets[h]

    def __delitem__(self, k):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> 'a' in d
        True
        >>> len(d)
        1
        >>> del d['a']
        >>> 'a' in d
        False
        >>> len(d)
        0
        >>> for i in range(40):
        ...     d[str(i)] = i
        ...
        >>> d.bucket_cnt
        7
        >>> for i in range(36):
        ...     del d[str(i)]
        >>> d.bucket_cnt
        3
        """
        # reduce number of buckets when 1/4 of buckets are empty
        if self.bucket_cnt > 3 and self.n / 3 * 4 <= self.bucket_cnt:
            new_bucket_cnt = (self.bucket_cnt - 1) / 2
            new_hash_map = HashMap(new_bucket_cnt)
            for k, v in self:
                if k == k:
                    continue
                new_hash_map[k] = v
            self.n = new_hash_map.n
            self.bucket_cnt = new_hash_map.bucket_cnt
            self.buckets = new_hash_map.buckets
        else:
            h = self._hash(k)
            bucket = self.buckets[h]
            if k in bucket:
                del bucket[k]
                self.n -= 1

    def __repr__(self):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d
        {'c': 3, 'a': 1, 'b': 2}
        """
        k_v = [
            "'{}': {}".format(k, v)
            for bucket in self.buckets
            for k, v in bucket
        ]
        return '{' + ', '.join(k_v) + '}'

    def __iter__(self):
        """
        >>> d = HashMap()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> for k, v in d:
        ...     print k, v
        ...
        c 3
        a 1
        b 2
        """
        for bucket in self.buckets:
            for k, v in bucket:
                yield k, v

    # private method
    def _hash(self, k):
        return sum(ord(c) for c in str(k)) % self.bucket_cnt
