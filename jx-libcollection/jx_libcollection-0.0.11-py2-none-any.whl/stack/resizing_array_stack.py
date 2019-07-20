class ResizingArrayStack(object):
    """
    This implementation uses a resizing array, which double the underlying array
    when it is full and halves the underlying array when it is one-quarter full.
    """

    def __init__(self, lst=None):
        """
        >>> stack = ResizingArrayStack(["a", 1, "b"])
        >>> stack.pop()
        'a'
        >>> stack.push('c')
        >>> stack
        ResizingArrayStack(['c', 1, 'b'])
        """
        self.capacity = 2
        self.resizing_array = [None] * self.capacity
        self.n = 0

        if lst:
            stack = ResizingArrayStack()
            for e in lst[::-1]:
                stack.push(e)

            self.capacity = stack.capacity
            self.resizing_array = stack.resizing_array
            self.n = stack.n

    def __len__(self):
        """
        >>> stack = ResizingArrayStack()
        >>> len(stack)
        0
        >>> stack.push('a')
        >>> len(stack)
        1
        """
        return self.n

    def __contains__(self, i):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> 'a' in stack
        True
        >>> 'c' in stack
        False
        """
        for j in self:
            if j == i:
                return True
        return False

    def __iter__(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> for i in stack:
        ...     print i
        ...
        b
        a
        """
        n = self.n
        while n > 0:
            n -= 1
            yield self.resizing_array[n]

    def __repr__(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack
        ResizingArrayStack(['b', 'a'])
        >>> print stack
        ResizingArrayStack(['b', 'a'])
        """
        return 'ResizingArrayStack([{}])'.format(', '.join(repr(i) for i in self))

    def push(self, i):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack.push('c')
        >>> stack
        ResizingArrayStack(['c', 'b', 'a'])
        """
        if self.n == self.capacity:
            self._resize(self.capacity*2)
        self.resizing_array[self.n] = i
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
        >>> stack.pop()
        Traceback (most recent call last):
            ...
        IndexError: pop from empty stack
        """
        if len(self) == 0:
            raise IndexError('pop from empty stack')
        if len(self) * 4 <= self.capacity:
            self._resize(self.capacity/2)
        self.n -= 1
        return self.resizing_array[self.n]

    @property
    def top(self):
        """
        >>> stack = ResizingArrayStack()
        >>> stack.top
        Traceback (most recent call last):
            ...
        IndexError: pop from empty stack
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
            resizing_array[i]= self.resizing_array[i]
        self.resizing_array = resizing_array
        self.capacity = m
