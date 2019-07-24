class LinearProbingKVStore(object):

    def __init__(self, capacity=4):
        self.capacity = capacity
        self.n = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

    def __len__(self):
        return self.n
    
    def __repr__(self):
        """
        >>> s = LinearProbingKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> s
        LinearProbingKVStore({'a': 1, 'b': 2, 'c': 3})
        """
        s = ', '.join('{}: {}'.format(repr(k), repr(v)) for k, v in self.items())
        return 'LinearProbingKVStore({%s})' % s

    def __iter__(self):
        """
        时间复杂度o(n)
        >>> s = LinearProbingKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> for i in s:
        ...     print(i)
        a
        b
        c
        """
        for k in self.keys:
            if k is not None:
                yield k
    
    def items(self):
        """
        时间复杂度o(n)
        >>> s = LinearProbingKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> for k, v in s.items():
        ...     print(k, v)
        a 1
        b 2
        c 3
        """
        for k, v in zip(self.keys, self.values):
            if k is not None:
                yield k, v

    def __contains__(self, k):
        """
        时间复杂度o(1)
        >>> s = LinearProbingKVStore()
        >>> s['a'] = 1
        >>> 'a' in s
        True
        >>> 'b' in s
        False
        """
        h = self._hash(k)
        while self.keys[h] is not None:
            if self.keys[h] == k:
                return True
            h = (h+1) % self.capacity
        return False

    def __setitem__(self, k, v):
        """
        平均时间复杂度o(1)
        应该有经过hash算法
        >>> s = LinearProbingKVStore()
        >>> s['a'] = 1
        >>> len(s)
        1
        >>> s.capacity
        4
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> s['d'] = 4
        >>> s['e'] = 5
        >>> s.capacity
        8
        """
        if len(self) >= self.capacity:
            self._resize(self.capacity*2)
        h = self._hash(k)
        while self.keys[h] is not None:
            if self.keys[h] == k:
                self.values[h] = v
                return
            h = (h+1) % self.capacity
        self.keys[h] = k
        self.values[h] = v
        self.n += 1

    def __getitem__(self, k):
        """
        >>> s = LinearProbingKVStore()
        >>> s['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['a']
        1
        >>> s['b']
        2
        """
        h = self._hash(k)
        while self.keys[h] is not None:
            if self.keys[h] == k:
                return self.values[h]
            h = (h+1) % self.capacity
        raise KeyError(k) 

    def __delitem__(self, k):
        """
        >>> s = LinearProbingKVStore()
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
        >>> s['c'] = 3
        >>> s['d'] = 4
        >>> s['e'] = 5
        >>> s['f'] = 6
        >>> s.capacity
        8
        >>> del s['b']
        >>> del s['c']
        >>> del s['d']
        >>> del s['e']
        >>> s.capacity
        4
        """
        if len(self) * 4 <= self.capacity:
            self._resize(self.capacity//2)
        h = self._hash(k)
        while True:
            if self.keys[h] is None:
                raise KeyError(k)
            if self.keys[h] == k:
                break
            h = (h+1) % self.capacity
        
        self._delete_kv_at_index(h)

         # rehash the keys in same bucket
        h = (h+1) % self.capacity

        while self.keys[h] is not None:
            self._rehash(h)
            h = (h+1) % self.capacity

    def _delete_kv_at_index(self, h):
        self.keys[h] = None
        self.values[h] = None
        self.n -= 1

    def _rehash(self, h):
        key = self.keys[h]
        value = self.values[h]
        self._delete_kv_at_index(h)
        self[key] = value

    def _hash(self, k):
        """
        >>> s = LinearProbingKVStore()
        >>> s._hash('a')
        1
        >>> s._hash('b')
        2
        """
        return sum(ord(i) for i in k) % self.capacity

    def _resize(self, capacity):
        """
        >>> s = LinearProbingKVStore()
        >>> s._resize(8)
        >>> s.capacity
        8
        """
        new = LinearProbingKVStore(capacity=capacity)
        for i in range(len(self.keys)):
            key = self.keys[i]
            if key is not None:
                new[key] = self.values[i]
        self.n = new.n
        self.capacity = new.capacity
        self.keys = new.keys
        self.values = new.values


if __name__ == '__main__':
    import doctest
    doctest.testmod()
