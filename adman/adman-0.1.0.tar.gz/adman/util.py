def single(seq, cond=None):
    """Extract a single item from a sequence matching condition `cond`

    Raises IndexError if there is not exactly one item matching the condition.
    """
    NOMATCH = object()

    result = single_or(seq, NOMATCH, cond)

    if result is NOMATCH:
        raise IndexError("No items found")
    return result


def single_or(seq, default, cond=None):
    """Extract a single item from a sequence matching condition `cond`

    Returns `default` if no item is found.

    Raises IndexError if there is more than one item matching the condition.
    """
    if cond is None:
        cond = lambda x: True

    NOMATCH = object()
    result = NOMATCH

    for x in seq:
        if not cond(x):
            continue
        if result is not NOMATCH:
            raise IndexError("Multiple items found")
        result = x

    if result is NOMATCH:
        result = default
    return result

def int_from_bytes(data, offset, length, byteorder):
    chunk = data[offset : offset+length]
    if len(chunk) != length:
        raise ValueError("Truncated data")

    return int.from_bytes(chunk, byteorder)
