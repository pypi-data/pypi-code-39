from linked_list import LinkedListKVstore


class HashMap(object):

    def __init__(self):
        self.length = 0
        self.bucket_count = 3
        self.arr = [LinkedListKVstore() for i in range(self.bucket_count)]

    def __len__(self):
        return self.length

    def _hash(self, k):
        """
        >>> h = HashMap()
        >>> h._hash('a')
        1
        >>> h._hash('b')
        2
        >>> h._hash('c')
        0
        """
        return sum(ord(i) for i in k) % self.bucket_count

    def __contains__(self, k):
        """
        >>> h = HashMap()
        >>> h['a'] = 1
        >>> 'a' in h
        True
        >>> 'b' in h
        False
        """
        h = self._hash(k)
        bucket = self.arr[h]
        return k in bucket

    def __setitem__(self, k, v):
        """
        >>> h = HashMap()
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> len(h)
        2
        >>> h['c'] = 3
        >>> len(h)
        3
        >>> h['a'] = 100
        >>> h['a']
        100
        """
        h = self._hash(k)
        bucket = self.arr[h]
        if k not in bucket:
            self.length += 1
        bucket[k] = v

    def __getitem__(self, k):
        """
        >>> h = HashMap()
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> h['a']
        1
        >>> h['b']
        2
        """
        h = self._hash(k)
        bucket = self.arr[h]
        if k in bucket:
            return bucket[k]

    def __delitem__(self, k):
        """
        >>> h = HashMap()
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> len(h)
        2
        >>> del h['a']
        >>> 'a' in h
        False
        >>> 'b' in h
        True
        >>> len(h)
        1
        """
        h = self._hash(k)
        bucket = self.arr[h]
        del bucket[k]
        self.length -= 1

    def __iter__(self):
        """
        >>> h = HashMap()
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> h['c'] = 3
        >>> for k, v in h:
        ...     print(k, v)
        c 3
        a 1
        b 2
        """
        for bucket in self.arr:
            for k,v in bucket:
                yield k, v 

    def __repr__(self):
        """
        >>> h = HashMap()
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> h['c'] = 3
        >>> h
        {'c': 3, 'a': 1, 'b': 2}
        """
        lst = []
        for bucket in self.arr:
            for k, v in bucket:
                lst.append('{}: {}'.format(repr(k), v))
        return '{' + ', '.join(lst) + '}'
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
