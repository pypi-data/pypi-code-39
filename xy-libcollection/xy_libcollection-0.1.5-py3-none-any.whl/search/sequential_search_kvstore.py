class KVNode(object):

    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.next = None

    def __repr__(self):
        """
        >>> n = KVNode('a', 1)
        >>> n
        KVNode('a', 1)
        """
        return 'KVNode({}, {})'.format(repr(self.key), repr(self.value))


class SequentialSearchKVStore(object):
    
    def __init__(self):
        self.n = 0
        self.head = KVNode(None, None)

    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> s =SequentialSearchKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> s
        SequentialSearchKVStore({'c': 3, 'b': 2, 'a': 1})
        """
        s = ', '.join('{}: {}'.format(repr(k), repr(v)) for k, v in self.iteritems())
        return 'SequentialSearchKVStore({%s})' % s 

    def __iter__(self):
        """
        >>> s = SequentialSearchKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> for i in s:
        ...     print(i)
        c
        b
        a
        """
        n = self.head.next
        while n:
            yield n.key
            n = n.next

    def iteritems(self):
        """
        >>> s = SequentialSearchKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> for k, v in s.iteritems():
        ...     print(k, v)
        c 3
        b 2
        a 1
        """
        n = self.head.next
        while n:
            yield n.key, n.value
            n = n.next

    def __contains__(self, k):
        """
        >>> s = SequentialSearchKVStore()
        >>> s['a'] = 1
        >>> s['b'] = 2
        >>> 'a' in s
        True
        """
        for i in self:
            if k == i:
                return True
        return False

    def __setitem__(self, k, v):
        """
        >>> s = SequentialSearchKVStore()
        >>> s['a'] = 1
        >>> len(s)
        1
        >>> s['b'] = 2
        >>> len(s)
        2
        """
        n = self._get_node(k)
        if n:
            n.value = value
        node = KVNode(k, v)
        node.next = self.head.next
        self.head.next = node
        self.n += 1

    def __getitem__(self, k):
        """
        >>> s = SequentialSearchKVStore()
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
        n = self._get_node(k)
        if not n:
            raise KeyError(k)
        return n.value

    def __delitem__(self, k):
        """
        >>> s = SequentialSearchKVStore()
        >>> s['a'] = 1 
        >>> s['b'] = 2
        >>> s['c'] = 3
        >>> len(s)
        3
        >>> del s['a']
        >>> len(s)
        2
        >>> 'a' in s
        False
        >>> del s['e']
        Traceback (most recent call last):
            ...
        KeyError: 'e'
        """
        h = self.head
        while h.next:
            if h.next.key == k:
                h.next = h.next.next
                self.n -= 1
                return
            h = h.next
        raise KeyError(k)
        
    def _get_node(self, k):
        n = self.head.next
        while n is not None:
            if n.key == k:
                return n
            n = n.next


if __name__ == '__main__':
    import doctest
    doctest.testmod()
