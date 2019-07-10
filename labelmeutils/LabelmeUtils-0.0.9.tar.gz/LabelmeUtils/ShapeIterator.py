from functools import reduce


class ShapeIterator:
    def __init__(self, shapes):
        self.shapes = shapes
        self.filter_fns = []
        self.iter = iter(self.shapes)

    def __iter__(self):
        self.iter = iter(self.shapes)
        return self

    def __next__(self):
        shape = self.iter.__next__()
        while not reduce(lambda prev, fn: prev and fn(shape), self.filter_fns, True):
            shape = self.iter.__next__()
        return shape

    def filter(self, fn):
        """
        Filter elements with function
        :param fn: (shape) => boolean
        :return: ShapeIterator
        """
        self.filter_fns.append(fn)
        return self


class ShapeImageIterator(ShapeIterator):
    def __init__(self, shapes, image, padding=None):
        ShapeIterator.__init__(self, shapes)
        self.image = image
        self.padding = padding

    def __next__(self):
        shape = super().__next__()
        return shape.crop_image(self.image, self.padding)
