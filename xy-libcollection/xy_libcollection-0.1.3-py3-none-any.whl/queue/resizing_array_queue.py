class ResizingArrayQueue(object):

    def __init__(self, lst=None, capacity=4):
        self.n = 0
        self.head = 0
        self.tail = 0
        self.capacity = capacity 
        self.lst = [None] * self.capacity

    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> q = ResizingArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q
        ResizingArrayQueue(['a', 'b'])
        """
        return 'ResizingArrayQueue([{}])'.format(', '.join(repr(i) for i in self))

    def __iter__(self):
        """
        >>> q = ResizingArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.enqueue('d')
        >>> for i in q:
        ...     print(i)
        a
        b
        c
        d
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.enqueue('e')
        >>> q.enqueue('f')
        >>> for i in q:
        ...     print(i)
        c
        d
        e
        f
        >>> q
        ResizingArrayQueue(['c', 'd', 'e', 'f'])
        """
        h = self.head
        for _ in range(self.n):
            yield self.lst[h]
            h = (h + 1) % self.capacity

    def __contains__(self, i):
        """
        >>> q = ResizingArrayQueue()
        >>> q.enqueue('a')
        >>> 'a' in q
        True
        >>> 'b' in q
        False
        """
        for j in self:
            if i == j:
                return True
        return False

    def enqueue(self, i):
        """
        >>> q = ResizingArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.enqueue('g')
        >>> q.enqueue('h')
        >>> q.capacity
        8
        >>> q.lst
        ['a', 'b', 'c', 'g', 'h', None, None, None]
        >>> 
        """
        if len(self) == self.capacity:
            self._resize(self.capacity*2)
        self.lst[self.tail] = i
        self.tail = (self.tail + 1) % self.capacity 
        self.n += 1

    def dequeue(self):
        """
        >>> q = ResizingArrayQueue(capacity=6)
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.dequeue()
        'c'
        >>> q.dequeue()
        Traceback (most recent call last):
            ...
        IndexError: queue underflow
        >>> q.enqueue('d')
        >>> q.enqueue('e')
        >>> q.enqueue('f')
        >>> q.dequeue()
        'd'
        >>> q.dequeue()
        'e'
        >>> len(q)
        1
        >>> q.capacity
        3
        """
        if self.n == 0:
            raise IndexError('queue underflow')
        if len(self) * 4 < self.capacity:
            self._resize(int(self.capacity/2))
        res = self.lst[self.head]
        self.head = (self.head + 1) % self.capacity 
        self.n -= 1
        return res

    @property
    def top(self):
        """
        >>> q = ResizingArrayQueue()
        >>> q.top
        Traceback (most recent call last):
            ...
        IndexError: top from empty queue
        >>> q.enqueue('a')
        >>> q.top
        'a'
        """
        if self.n == 0:
            raise IndexError('top from empty queue')
        return self.lst[self.head]

    def _resize(self, n):
        """
        >>> q = ResizingArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q
        ResizingArrayQueue(['a', 'b', 'c'])
        >>> q._resize(6)
        >>> q.lst
        ['a', 'b', 'c', None, None, None]
        """
        q = ResizingArrayQueue(capacity=n)
        for e in self:
            q.enqueue(e)
        self.n = q.n
        self.head = q.head
        self.tail = q.tail
        self.lst = q.lst
        self.capacity = q.capacity


if __name__ == '__main__':
    import doctest
    doctest.testmod()
