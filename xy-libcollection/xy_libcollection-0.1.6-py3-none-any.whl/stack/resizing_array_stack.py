class ResizingArrayStack(object):
    """
    """

    def __init__(self):
        self.n = 0
        self.capacity = 2
        self.resizing_array = [None] * self.capacity

    def __len__(self):
        return self.n

    def __contains__(self, i):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> 'a' in stack
        True
        >>> 'b' in stack
        True
        >>> 'c' in stack
        False
        """
        for j in self:
            if i == j:
                return True
        return False

    def __iter__(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> for i in stack:
        ...     print(i)
        ...
        b
        a
        """
        n = self.n
        while n > 0:
            n -= 1
            yield self.resizing_array[n]

    def __str__(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack
        ResizingArrayStack(['b', 'a'])
        >>> print(stack)
        ResizingArrayStack(['b', 'a'])
        """
        return 'ResizingArrayStack([{}])'.format(', '.join(repr(i) for i in self))

    __repr__ = __str__

    def push(self, item):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> len(stack)
        2
        >>> stack.capacity
        2
        >>> stack.n
        2
        >>> stack.push('c')
        >>> stack.push('d')
        >>> len(stack)
        4
        >>> stack.capacity
        4
        >>> stack.push('e')
        >>> stack.push('f')
        >>> len(stack)
        6
        >>> stack.capacity
        8
        >>> stack.push('g')
        >>> stack.push('h')
        >>> len(stack)
        8
        >>> stack.capacity
        8
        """
        if self.n == self.capacity:
            self._resize(self.capacity*2)
        self.resizing_array[self.n] = item
        self.n += 1

    def pop(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack.push('c')
        >>> stack.push('d')
        >>> stack.push('e')
        >>> stack.push('f')
        >>> stack.push('g')
        >>> stack.push('h')
        >>> len(stack)
        8
        >>> stack.pop()
        'h'
        >>> stack.pop()
        'g'
        >>> stack.pop()
        'f'
        >>> stack.pop()
        'e'
        >>> stack.pop()
        'd'
        >>> stack.pop()
        'c'
        >>> len(stack)
        2
        >>> stack.capacity
        8
        >>> stack.pop()
        'b'
        >>> len(stack)
        1
        >>> stack.capacity
        4
        >>> stack.pop()
        'a'
        >>> len(stack)
        0
        >>> stack.capacity
        2
        """
        if len(self) == 0:
            raise IndexError('pop from empty stack')
        if len(self) * 4 <= self.capacity:
            m = int(self.capacity / 2)
            self._resize(m)
        self.n -= 1
        return self.resizing_array[self.n]

    @property
    def top(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.top
        'a'
        >>> stack.push('b')
        >>> stack.top
        'b'
        """
        if len(self) == 0:
            raise IndexError('pop from empty stack')
        return self.resizing_array[self.n-1]

    def _resize(self, m):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack._resize(6)
        >>> stack.resizing_array
        ['a', 'b', None, None, None, None]
        >>> stack.capacity
        6
        >>> len(stack)
        2
        >>> stack
        ResizingArrayStack(['b', 'a'])
        """
        resizing_array = [None] * m
        for i in range(self.n):
            resizing_array[i] = self.resizing_array[i]
        self.resizing_array = resizing_array
        self.capacity = m

if __name__ == '__main__':
    import doctest
    doctest.testmod()

