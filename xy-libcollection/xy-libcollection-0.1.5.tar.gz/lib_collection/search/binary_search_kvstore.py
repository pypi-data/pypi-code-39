class NoneNode(object):
    pass
    
    def __repr__(self):
        return 'NoneNode()'
    

none = NoneNode()


class BinarySearchKVStore(object):

    def __init__(self, capacity=2):
        self.n = 0
        self.capacity = capacity
        self.keys = [none] * self.capacity
        self.values = [none] * self.capacity


    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d
        BinarySearchKVStore({'a': 1, 'b': 2, 'c': 3})
        """
        s = ', '.join('{}: {}'.format(repr(k), v) for k, v in self.items())
        return 'BinarySearchKVStore({%s})' % s

    def __iter__(self):
        """
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> for i in d:
        ...     print(i)
        ...
        a
        b
        c
        """
        for i in range(len(self)):
            yield self.keys[i]

    def items(self):
        """
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> for k, v in d.items():
        ...     print(k, v)
        ...
        a 1
        b 2
        c 3
        """
        for i in range(len(self)):
            yield self.keys[i], self.values[i]

    def __contains__(self, key):
        """
        >>> d = BinarySearchKVStore()
        >>> 'a' in d
        False
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> 'a' in d
        True
        """
        i = self.index(key)
        if i < len(self) and self.keys[i] == key:
            return True
        return False

    @property
    def min(self):
        """
        >>> # 1. test min from empty kvstore raise index error
        >>> d = BinarySearchKVStore()
        >>> d.min
        Traceback (most recent call last):
            ...
        IndexError: underflow
        >>> # 2. test get min
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d.min
        'a'
        """
        if len(self) == 0:
            raise IndexError('underflow')
        return self.keys[0]

    @property
    def max(self):
        """
        >>> # 1. test max from empty kvstore raise index error
        >>> d = BinarySearchKVStore()
        >>> d.min
        Traceback (most recent call last):
            ...
        IndexError: underflow
        >>> # 2. test get max
        >>> d['a'] = 3
        >>> d['b'] = 1
        >>> d['c'] = 2
        >>> d.max
        'c'
        """
        if len(self) == 0:
            raise IndexError('underflow')
        return self.keys[self.n-1]

    def del_min(self):
        """
        >>> #1. test del_min from empty kvstore raise index error
        >>> d = BinarySearchKVStore()
        >>> d.del_min()
        Traceback (most recent call last):
            ...
        IndexError: underflow
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d.min
        'a'
        >>> d.del_min()
        >>> d.min
        'b'
        >>> 
        """
        if len(self) == 0:
            raise IndexError('underflow')
        del self[self.min]

    def del_max(self):
        """
        >>> #1. test del_max from empty kvstore raise index error
        >>> d = BinarySearchKVStore()
        >>> d.del_max()
        Traceback (most recent call last):
            ...
        IndexError: underflow
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d.max
        'c'
        >>> d.del_max()
        >>> d.max
        'b'
        >>> 
        """
        if len(self) == 0:
            raise IndexError('underflow')
        del self[self.max]

    def __setitem__(self, key, value):
        """
        >>> # 1.test key in keys
        >>> d = BinarySearchKVStore()
        >>> d.keys = [1, 2]
        >>> d.values = ['a', 'b']
        >>> d.n = 2
        >>> d[1] = 'c'
        >>> d.values
        ['c', 'b']
        >>> # 2.test full and resize
        >>> d = BinarySearchKVStore()
        >>> d.keys = [1, 2]
        >>> d.values = ['a', 'b']
        >>> d.n = 2
        >>> d[3] = 'c'
        >>> d.n
        3
        >>> d.keys
        [1, 2, 3, NoneNode()]
        >>> d.values
        ['a', 'b', 'c', NoneNode()]
        >>> # 3. test insert new key in the end
        >>> d = BinarySearchKVStore()
        >>> d.keys = [1, 2]
        >>> d.values = ['a', 'b']
        >>> d.n = 2
        >>> d[3] = 'c'
        >>> d.keys
        [1, 2, 3, NoneNode()]
        >>> d.values
        ['a', 'b', 'c', NoneNode()]
        >>> # 4.test insert new key in the middle
        >>> d = BinarySearchKVStore()
        >>> d.keys = [1, 3]
        >>> d.values = ['a', 'c']
        >>> d.n = 2
        >>> d[2] = 'b'
        >>> d.keys
        [1, 2, 3, NoneNode()]
        >>> d.values
        ['a', 'b', 'c', NoneNode()]
        >>> # test insert new key in the head
        >>> d = BinarySearchKVStore()
        >>> d.keys = [2, 3]
        >>> d.values = ['b', 'c']
        >>> d.n = 2
        >>> d[1] = 'a'
        >>> d.keys
        [1, 2, 3, NoneNode()]
        >>> d.values
        ['a', 'b', 'c', NoneNode()]
        """
        # if key in keys
        i = self.index(key)
        if i < len(self) and self.keys[i] == key:
            self.values[i] = value
            return

        # test full and resize
        if len(self) == self.capacity:
            self._resize(self.capacity*2)

        for j in range(len(self), i, -1):
            self.keys[j] = self.keys[j-1]
            self.values[j] = self.values[j-1]
        
        #insert new key
        self.keys[i] = key
        self.values[i] = value
        self.n += 1

    def __getitem__(self, key):
        """
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['a']
        1
        >>> d['b']
        2
        >>> d['c']
        Traceback (most recent call last):
            ...
        KeyError: 'c'
        """
        i = self.index(key)
        if i < len(self) and self.keys[i] == key:
            return self.values[i]
        raise KeyError(key)

    def __delitem__(self, key):
        """
        >>> d = BinarySearchKVStore()
        >>> d['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        >>> #2 test delete item that exists
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d.keys
        ['a', 'b', 'c', NoneNode()]
        >>> del d['a']
        >>> d.keys
        ['b', 'c', NoneNode(), NoneNode()]
        >>> #3 test delete item and resize down
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d['d'] = 4
        >>> d['e'] = 5
        >>> del d['a']
        >>> del d['b']
        >>> d.capacity
        8
        >>> del d['c']
        >>> d.capacity
        4
        >>> del d['d']
        >>> d.capacity
        2
        """
        i = self.index(key)
        if i == len(self) and self.keys[i] != key:
            raise KeyError(key)
        for j in range(i, len(self)-1):
            self.keys[j] = self.keys[j+1]
            self.values[j] = self.values[j+1]
        self.n -= 1
        self.keys[self.n] = none
        self.values[self.n] = none

        if len(self) * 4 <= self.capacity and len(self):
            self._resize(self.capacity//2)

    def index(self, key):
        """
        >>> b = BinarySearchKVStore()
        >>> b.n = 3
        >>> b.keys = [1, 2, 3]
        >>> b.index(2)
        1
        >>> b.index(1.5)
        1
        >>> b.index(2.5)
        2
        """
        lo = 0
        hi = self.n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if key == self.keys[mid]:
                return mid
            elif key < self.keys[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        return lo

    def _resize(self, capacity):
        """
        >>> d = BinarySearchKVStore()
        >>> d.n = 2
        >>> d.keys = [1, 2]
        >>> d.values = ['a', 'b']
        >>> d._resize(4)
        >>> d.keys
        [1, 2, NoneNode(), NoneNode()]
        >>> d.values
        ['a', 'b', NoneNode(), NoneNode()]
        """
        keys = [none] * capacity
        values = [none] * capacity
        for i in range(len(self)):
            keys[i] = self.keys[i]
            values[i] = self.values[i]
        self.keys = keys
        self.values = values
        self.capacity = capacity

    def get_key_at_index(self, i):
        """
        >>> d = BinarySearchKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d['c'] = 3
        >>> d.get_key_at_index(3)
        Traceback (most recent call last):
            ...
        IndexError: 3
        >>> d.get_key_at_index(1)
        'b'
        """
        if not 0 <= i < len(self):
            raise IndexError(i)
        return self.keys[i]

    def floor(self, key):
        """
        Return the largest key in kvstore that is less than or equal to key
        >>> d = BinarySearchKVStore()
        >>> d[1] = 'a'
        >>> d[2] = 'b'
        >>> d[3] = 'c'
        >>> d.floor(2)
        2
        >>> d.floor(1.1)
        1
        >>> d.floor(4)
        3
        >>> d.floor(0.9)
        """
        i = self.index(key)
        if i < len(self) and self.keys[i] == key:
            return self.keys[i]
        elif i == 0:
            return  # so key in this kvstore cannot be None
        return self.keys[i-1]

    def ceiling(self, key):
        """
        Return the smallest key in kvstore that is greater than or equal to key
        >>> d = BinarySearchKVStore()
        >>> d[1] = 'a'
        >>> d[2] = 'b'
        >>> d[3] = 'c'
        >>> d.ceiling(1.5)
        2
        >>> d.ceiling(0.5)
        1
        >>> d.ceiling(2)
        2
        >>> d.ceiling(5)
        """
        i = self.index(key)
        if i == len(self):
            return
        return self.keys[i]

    def size(self, key1, key2):
        """
        return the numbers of keys in this kvstore that min(key1, key2) <= key <= max(key1, key2)
        >>> d = BinarySearchKVStore()
        >>> d[1] = 'a'
        >>> d[2] = 'b'
        >>> d[3] = 'c'
        >>> d.size(1.5, 2.5)
        1
        >>> d.size(1.5, 3)
        2
        >>> d.size(1, 3)
        3
        """
        lo = min(key1, key2)
        hi = max(key1, key2)
        i = self.index(lo)
        j = self.index(hi)
        if hi in self:
            return j - i + 1
        return j - i


if __name__ == '__main__':
    import doctest
    doctest.testmod()
