from .Interval import *

d = Intervals(([1, 3], [4, 6]))
d.marge()
print(d)
a = Intervals(([2, 4], [4, 5]))
print(a in d)
