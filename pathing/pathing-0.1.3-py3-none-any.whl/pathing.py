import collections


__all__ = ('derive',)


_top = float('inf')


def derive(root, old = None, get = None, min = - _top, max = _top):

    if old is None:

        old = ()

    length = len(old)

    if not get is None:

        root = get(root, old)

    if not length < min:

        yield (old, root)

    if not isinstance(root, collections.Mapping):

        return

    if length + 1 > max:

        return

    for (key, value) in root.items():

        new = old + (key,)

        yield from derive(value, old = new, get = get, min = min, max = max)
