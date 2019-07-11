

def depths(mdk, depth_cutoff=10):
    """
    m, d, k are the iterables returned from pytabix region query
    """

    heap = [next(v) for v in mdk]

    while len(heap) > 0:

        chrom = heap[0].chrom
        istart = max(h.start for h in heap)
        iend = min(h.end for h in heap)

        yn = all(h.depth >= depth_cutoff for h in heap)
        yield (chom, istart, iend, yn)

        try:
            heap = [h if h.end != iend else next(mdk[i]) for i, h in enumerate(heap)]
        except StopIteration:
            # TODO: make sure that when the stop iteration occurs that iend is
            # the end of the requested region.
            break
