class ArrayQueue(object):

    def __init__(self, lst=None, capacity=4):
        """
        >>> q = ArrayQueue(['a', 'b', 'c'])
        >>> q.n
        3
        >>> q.head
        0
        >>> q.tail
        3
        """
        self.n = 0
        self.capacity = capacity 
        self.lst = [None] * self.capacity
        self.head = 0
        self.tail = 0

        if lst:
            q = ArrayQueue(capacity=capacity)
            for i in lst:
                q.enqueue(i)
            self.lst = q.lst
            self.n = q.n
            self.head = q.head
            self.tail = q.tail
    
    def __len__(self):
        """
        >>> q = ArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.enqueue('d')
        >>> q.tail
        0
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.dequeue()
        'c'
        >>> q.head
        3
        >>> len(q)
        1
        >>> q.enqueue('e')
        >>> q.enqueue('f')
        >>> len(q)
        3
        """
        return self.n

    def __repr__(self):
        """
        >>> q = ArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.enqueue('d')
        >>> q
        ArrayQueue(['a', 'b', 'c', 'd'])
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.enqueue('e')
        >>> q
        ArrayQueue(['c', 'd', 'e'])
        """
        return 'ArrayQueue([{}])'.format(', '.join(repr(i) for i in self))

    def __iter__(self):
        """
        >>> q = ArrayQueue()
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
        >>> for i in q:
        ...     print(i)
        c
        d
        e
        """
        n = self.head
        for _ in range(len(self)):
            yield self.lst[n]
            n = (n + 1) % self.capacity
            
    def __contains__(self, i):
        """
        >>> q = ArrayQueue()
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
        >>> q = ArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.enqueue('d')
        >>> q.enqueue('e')
        Traceback (most recent call last):
            ...
        IndexError: queue overflow
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> len(q)
        2
        """
        if len(self) == self.capacity:
            raise IndexError ('queue overflow')
        self.lst[self.tail] = i
        self.tail = (self.tail + 1) % self.capacity 
        self.n += 1

    def dequeue(self):
        """
        >>> q = ArrayQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.enqueue('d')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.dequeue()
        'c'
        >>> q.enqueue('e')
        >>> q.dequeue()
        'd'
        >>> q.dequeue()
        'e'
        >>> q.dequeue()
        Traceback (most recent call last):
            ...
        IndexError: dequeue from empty queue
        """
        if len(self) == 0:
            raise IndexError('dequeue from empty queue')
        res = self.lst[self.head]
        self.head = (self.head + 1) % self.capacity
        self.n -= 1
        return res

    @property
    def top(self):
        """
        >>> q = ArrayQueue()
        >>> q.enqueue('a')
        >>> q.top
        'a'
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.top
        'a'
        """
        if len(self) == 0:
            raise IndexError('top from empty queue')
        return self.lst[self.head]
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()
