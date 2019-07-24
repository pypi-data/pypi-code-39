from sequential_search_kvstore import SequentialSearchKVStore


class SeparateChainingHashKVStore(object):

    _item_count_per_bucket = 1

    def __init__(self, bucket_count=4):
        self.n = 0
        self.bucket_count = bucket_count
        self.lst = [SequentialSearchKVStore() for _ in range(self.bucket_count)]

    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> s
        SeparateChainingHashKVStore({'a': 1, 'b': 2, 'c': 3})
        """
        s = ', '.join('{}: {}'.format(repr(k), repr(v)) for k, v in self.items())
        return 'SeparateChainingHashKVStore({%s})' % s

    def __iter__(self):
        """
        >>> s = SeparateChainingHashKVStore()
        """
        for kvstore in self.lst:
            for k in kvstore:
                yield k
    
    def items(self):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> for k, v in s.items():
        ...     print(k, v)
        a 1
        b 2
        c 3
        """
        for kvstore in self.lst:
            for k, v in kvstore.iteritems():
                yield k, v

    def __contains__(self, k):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s['a'] = 1
        >>> 'a' in s
        True
        >>> 'b' in s
        False
        """
        h = self._hash(k)
        b = self.lst[h]
        if k in b:
            return True
        return False

    def __setitem__(self, k, v):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s['a'] = 1
        >>> len(s)
        1
        >>> s['b'] = 2
        >>> len(s)
        2
        >>> s['a'] = 3
        >>> len(s)
        2
        >>> s['c'] = 4
        >>> s['d'] = 5
        >>> s.bucket_count
        4
        >>> s['e'] = 6
        >>> s.bucket_count
        8
        """
        if self.n >= self.bucket_count * self._item_count_per_bucket:
            self._resize(self.bucket_count*2)
        i = self._hash(k)
        d = self.lst[i]
        if k not in d:
            self.n += 1
        d[k] = v

    def __getitem__(self, k):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['a']
        1
        >>> s['b']
        2
        >>> s['c']
        Traceback (most recent call last):
            ...
        KeyError: 'c'
        """
        h = self._hash(k)
        b = self.lst[h]
        if k not in b:
            raise KeyError(k)
        return b[k]

    def __delitem__(self, k):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> len(s)
        2
        >>> del s['a']
        >>> len(s)
        1
        >>> del s['c']
        Traceback (most recent call last):
            ...
        KeyError: 'c'
        """
        if self.n * 4 <= self.bucket_count * self._item_count_per_bucket:
            self._resize(self.bucket_count//2)
        h = self._hash(k)
        b = self.lst[h]
        if k not in b:
            raise KeyError(k)
        del b[k]
        self.n -= 1

    def _hash(self, k):
        """
        >>> s = SeparateChainingHashKVStore()
        >>> s._hash('a')
        1
        >>> s._hash('b')
        2
        """
        return sum(ord(i) for i in k) % self.bucket_count 

    def _resize(self, bucket_count):
        s = SeparateChainingHashKVStore(bucket_count=bucket_count)
        for k, v in self.items():
            s[k] = v
        self.bucket_count = bucket_count
        self.lst = s.lst
        self.n = s.n


if __name__ == '__main__':
    import doctest
    doctest.testmod()
