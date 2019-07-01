_MAX_COORDS = 1e18

EMPTY_BBOX = (_MAX_COORDS, _MAX_COORDS, -_MAX_COORDS, -_MAX_COORDS)


class BBox(object):
    arr = []

    def __init__(self, arr=None):
        if not arr:
            arr = EMPTY_BBOX
        if not isinstance(arr, list) and not isinstance(arr, tuple):
            raise TypeError("invalid coordinates")
        if len(arr) != 4:
            raise ValueError("invalid coordinates")
        if arr[0] > arr[2] or arr[1] > arr[3]:
            arr = EMPTY_BBOX
        for obj in arr:
            item = float(obj)
            self.arr.append(item)

    def empty(self):
        return self.arr[0] > self.arr[2] or self.arr[1] > self.arr[3]

    def intersect(self, other):
        if not isinstance(other, BBox):
            raise TypeError("invalid bbox")
        return BBox((max(self.arr[0], other.arr[0]), max(self.arr[1], other.arr[1]),
                     min(self.arr[2], other.arr[2]), min(self.arr[3], other.arr[3])))

    def union(self, other):
        if not isinstance(other, BBox):
            raise TypeError("invalid bbox")
        return BBox((min(self.arr[0], other.arr[0]), min(self.arr[1], other.arr[1]),
                     max(self.arr[2], other.arr[2]), max(self.arr[3], other.arr[3])))
