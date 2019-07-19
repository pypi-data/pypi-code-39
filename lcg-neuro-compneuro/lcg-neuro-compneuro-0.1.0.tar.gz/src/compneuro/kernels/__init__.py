import numpy


def gaussian(sigma, mu=0.0, rate=1.0, devs=2):
    """Produces a symmetric normalized Gaussian kernel.

    Parameters
    ----------
    sigma: number
        Standard deviation.

    mu: number
        Kernel center.

    rate: number
        Kernel support sampling rate. The inverse of this quantity corresponds to the distance between adjacent points
        in the kernel's support.

    devs: int
        The kernel support is truncated this number of standard deviations away from the center, on the side that is
        furthest from the origin. Normally, if ``devs >= 2``, values on both ends will be considerably close to zero
        even if the kernel is shifted.

    Returns
    -------
    kernel: :class:`numpy.ndarray`

    Note
    ----
    * Output shape is influenced by all parameters.
    * The number of kernel points is always odd.
    * The kernel is normalized in the discrete sense, e.g. the sum of all points equals 1.
    """
    x_min = mu - devs * sigma
    x_max = mu + devs * sigma
    x_amp = max(abs(x_min), abs(x_max))

    points = int(round(2 * x_amp * rate)) | 1
    x = (numpy.arange(points) - points // 2) / rate
    y = numpy.exp(-((x - mu) / sigma) ** 2)

    return y / numpy.sum(y)
