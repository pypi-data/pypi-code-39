class Stream:
    """
    Stream is abstract stream for string and list
    """
    EOF = (-1)

    def __init__(self, src):
        if not isinstance(src, (str, list)):
            raise TypeError('invalid type of source in absstream.stream.Stream')

        self._src = src
        self._limit = len(src)
        self._index = 0

    def eof(self):
        return self._index >= self._limit or self._index < 0

    def get(self):
        if self.eof():
            return self.EOF

        ch = self._src[self._index]
        self.next()
        return ch

    def cur(self, ofs=0):
        if not isinstance(ofs, int):
            raise TypeError('invalid offset in cur of absstream.stream.Stream')
        
        i = self._index + ofs
        if i < self._limit and i >= 0:
            return self._src[i]
        return self.EOF

    def prev(self):
        if self._index > 0:
            self._index -= 1

    def next(self):
        if self._index < self._limit:
            self._index += 1

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, val):
        self._index = val
