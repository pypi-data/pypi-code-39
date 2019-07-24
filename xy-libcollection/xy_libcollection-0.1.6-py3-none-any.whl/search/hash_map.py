from linked_list import LinkedListKVstore


class HashMap(object):

    _item_count_per_bucket = 10

    def __init__(self, bucket_count=3):
        self.length = 0
        self.bucket_count = bucket_count 
        self.arr = [LinkedListKVstore() for _ in range(self.bucket_count)]

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
        >>> for i in range(40):
        ...     h[str(i)] = i
        ...
        >>> h.bucket_count
        7
        """
        if self.bucket_count * self._item_count_per_bucket <= self.length:
            new_bucket_count = self.bucket_count * 2 + 1
            new_hash_map = HashMap(new_bucket_count) 
            new_hash_map[k] = v
            for _k, _v in self:
                new_hash_map[_k] = _v
            self.length = new_hash_map.length
            self.bucket_count = new_hash_map.bucket_count
            self.arr = new_hash_map.arr
        else:
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
        >>> for i in range(40):
        ...     h[str(i)] = i
        ...
        >>> h.bucket_count
        7
        >>> for i in range(40):
        ...     del h[str(i)]
        ...
        >>> h.bucket_count
        3
        """
        if self.bucket_count > 3 and self.length <= int(self.bucket_count / 2):
            new_bucket_count = int((self.bucket_count - 1) / 2)
            new_hash_map = HashMap(new_bucket_count)
            for _k, _v in self:
                if _k == k:
                    continue
                new_hash_map[_k] = _v
            self.length = new_hash_map.length
            self.bucket_count = new_hash_map.bucket_count
            self.arr = new_hash_map.arr
        else:
            h = self._hash(k)
            bucket = self.arr[h]
            if k in bucket:
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
            for k, v in bucket:
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
