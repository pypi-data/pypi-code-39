import math
import numpy
import scipy.signal


def cross_correlation(x, y, input_norm="zncc", output_norm="coef"):
    r"""Computes cross-correlation between discrete time series.

    Computes the cross-correlation :math:`x \star y` of one-dimensional discrete time series :math:`x` and :math:`y`.
    Currently, it only supports full convolution, that is, by passing :code:`mode='full'` to
    :func:`scipy.signal.correlate`.

    Parameters
    ----------
    x: :class:`numpy.ndarray`
        Discrete time series.

    y: :class:`numpy.ndarray`
        Discrete time series.

    input_norm: str
        Input normalization applied before correlation computation. Accepted modes:

        ncc:
            *Normalized cross-correlation*. Input series :math:`x, y` are divided by their standard deviations. If they
            are non-negative, the result will also be non-negative.

        none:
            Default. No normalization, the input series are correlated as they are given. If they are non-negative, the
            result will also be non-negative.

        zncc:
            *Zero-normalized cross-correlation*. Input series :math:`x, y` are demeaned, then divided by their
            respective standard deviations.

    output_norm: str
        Output normalization after correlation computation. Accepted modes:

        coef:
            Two copies of :math:`y` are shifted according to the location of the maximum and minimum peaks, namely
            :math:`y^+` and :math:`y^-`. The correlation coefficients :math:`C(x, y^+)` and :math:`C(x, y^-)` are
            computed and :math:`z` is finally normalized with values ranging in :math:`[C(x, y^-), C(x, y^+)]`. Hence,
            this mode always restricts :math:`z` to :math:`[-1, 1]`. **Note:** This mode only works if
            :code:`len(x) == len(y)`.

        length:
            Divides the output by :code:`len(x)`.

        none:
            Default. No normalization.

    Return
    ------
    cross_correlation: :class:`numpy.ndarray`

    Notes
    -----
    Scipy's defintion of cross-correlation considers that negative lags represent shifting the second operand to the
    left and positive lag represents shifting the second operand to the right. Put in math notation, this means cross-
    correlation is defined in Scipy as

    .. math::

        (f \star g)(\tau) = \int_{-\infty}^{\infty} f^{*}(t) g(t - \tau) {\rm d}t

    So when we look for the optimal alignment of functions :math:`f,g` using :func:`scipy.signal.correlate`,  we should
    interpret a positive value of the lag :math:`\tau` as ":math:`f` is best matched by :math:`g` if it is earlier than
    :math:`f` by an amount of time :math:`\tau`", and a positive value of the lag as ":math:`f` is best matched by
    :math:`g` if it is later than :math:`f` by an amout of time :math:`\tau`".

    This is completely counter intuitive, as it corresponds to interpreting :math:`f` as the *received signal* and
    :math:`g` as the *emitted signal*, after all a positive lag for the received signal should mean it is *in fact*
    received, whereas a negative lag should indicate it is actually the emitted signal. Therefore, this function inverts
    the result of :func:`scipy.signal.correlate`, restoring a more intelligible definition of the operation of cross-
    correlation as

    .. math::

        (f \star g)(\tau) = \int_{-\infty}^{\infty} f^{*}(t) g(t + \tau) {\rm d}t

    so that, when we get positive :math:`\tau` values, that really means the *lag*, or *delay* of :math:`g` (the
    receiver) relative to :math:`f` (the emitter).
    """
    if input_norm == "ncc":
        x = x / numpy.std(x)
        y = y / numpy.std(y)
    elif input_norm == "zncc":
        x = (x - numpy.mean(x)) / numpy.std(x)
        y = (y - numpy.mean(y)) / numpy.std(y)

    try:
        units = x.units ** 2
    except AttributeError:
        units = 1.0

    z = scipy.signal.correlate(x, y, mode="full")[::-1]

    if output_norm == "coef":
        i_max = numpy.argmax(z) - len(z) // 2
        i_min = numpy.argmin(z) - len(z) // 2

        if i_max < 0:
            z_max = numpy.corrcoef(x[-i_max:], y[:i_max])[0, 1]
        elif i_max > 0:
            z_max = numpy.corrcoef(x[:-i_max], y[i_max:])[0, 1]
        else:
            z_max = numpy.corrcoef(x, y)[0, 1]

        if i_min < 0:
            z_min = numpy.corrcoef(x[-i_min:], y[:i_min])[0, 1]
        elif i_min > 0:
            z_min = numpy.corrcoef(x[:-i_min], y[i_min:])[0, 1]
        else:
            z_min = numpy.corrcoef(x, y)[0, 1]

        return z_min + (z_max - z_min) * (z - numpy.min(z)) / (
            numpy.max(z) - numpy.min(z)
        )
    elif output_norm == "length":
        return z * units / len(x)
    else:
        return z * units


def firing_rate(spikes, kernel, rate=1.0, extend="mean"):
    r"""Computes the mean firing rate of a collection of spike histograms.

    Given spike trains ``st`` for one or more trials and a ``kernel``, computes the mean firing rate by convolving the
    mean spike histogram with the kernel, which does not need to be normalized (e.g. the sum of its entries must not
    necessarily be equal to one).

    Parameters
    ----------
    spikes: sequence
        A ``(M, N)`` or ``(N,)`` array of spike histograms with ``N`` bins over ``M`` trials.

    kernel: sequence
        A set of weights for the spike bin counts, preferably symmetric. Most usually, the sum of its elements should be
        equal to one. It is also possible to have the sum of its elements equal to the intended sampling rate, and pass
        the default value of ``rate = 1`` to get a correctly scaled result. If the kernel is not symmetric, the
        convolution is computed by aligning the kernel at the element immediately to the right of its center, that is,
        alignment is always performed at the element ``kernel[len(kernel)//2]``.

    rate: float
        If given, denotes the sampling rate, that is, its inverse corresponds to the width of the spike bins. The
        resulting firing rate is multiplied by this quantity to provide the correct scale.

    extend:
        Determines how to compute the firing rate near borders. Accepted values:

        border:
            Extend the borders of the mean spike histogram with the own border elements. Convolution is then computed by
            passing ``mode='valid'`` to :func:`numpy.convolve`.

        mean:
            Extend the mean spike histogram with the mean value of all spike histograms, avoiding steep falls near the
            borders and preserving the mean number of spikes. Convolution is computed by passing ``mode='valid'`` to
            :func:`numpy.convolve`.

        none:
            No extension of border values. Convolution is computed by passing ``mode='same'`` to :func:`numpy.convolve`.
            It is the same as passing ``extend=0``.

        :class:`float`:
            If a number is passed, the borders are extended with this number. Then, convolution is computed by passing
            ``mode='valid'`` to :func:`numpy.convolve`.

    Returns
    -------
    :class:`numpy.ndarray`
        The output has shape ``(N,)`` and type ``numpy.float64``, where ``N`` is the same as the input ``st``.
    """

    mean_st = numpy.mean(numpy.atleast_2d(spikes), axis=0)

    if extend == "border":
        mode = "valid"
        mean_st = numpy.hstack(
            [
                numpy.repeat(mean_st[0], len(kernel) // 2),
                mean_st,
                numpy.repeat(mean_st[-1], (len(kernel) - 1) // 2),
            ]
        )
    elif extend == "none":
        mode = "same"
    elif extend == "mean":
        mean_st = numpy.hstack(
            [
                numpy.repeat(numpy.mean(mean_st), len(kernel) // 2),
                mean_st,
                numpy.repeat(numpy.mean(mean_st), (len(kernel) - 1) // 2),
            ]
        )
        mode = "valid"
    else:
        mean_st = numpy.hstack(
            [
                numpy.repeat(extend, len(kernel) // 2),
                mean_st,
                numpy.repeat(extend, (len(kernel) - 1) // 2),
            ]
        )
        mode = "valid"

    return rate * numpy.convolve(mean_st, kernel[::-1], mode=mode)


def spike_hist(ts, rate, duration=None):
    r"""Computes spike histograms from spike timestamps.

    Parameters
    ----------
    ts: :class:`numpy.ndarray` or sequence
        List of spike timestamps. If a one-dimensional vector or sequence is given, it is assumed that it contains
        timestamps from a single trial. If a sequence of sequences is given, it is assumed that each sub-sequence
        constitutes a separate trial.

    rate: number
        Sampling rate for spikes. Spikes are binned in intervals as wide as the inverse of this quantity.

    duration: number
        Duration of recording session. If not informed, it is assumed to be at least as long as the last timestamp.

    Returns
    -------
    :class:`numpy.ndarray`
        Spike histogram. If the input is a single trial, the output shape is ``N``, otherwise, it is ``(M,N)``,
        where ``M = len(ts)`` and

        .. math::
            N = \left\lceil \frac{\textrm{duration}}{\textrm{rate}} \right\rceil
    """
    if duration is None:
        duration = numpy.max(numpy.hstack(ts))
    length = int(math.ceil(duration * rate))
    bins = numpy.arange(length + 1) / rate

    try:
        len(ts[0])
        spike_trains = numpy.zeros((len(ts), length))
        for i, trial_ts in enumerate(ts):
            try:
                spike_trains[i, :] = numpy.histogram(trial_ts.to(bins.u), bins=bins)[0]
            except AttributeError:
                spike_trains[i, :] = numpy.histogram(trial_ts, bins=bins)[0]
    except TypeError:
        try:
            spike_trains = numpy.histogram(ts.to(bins.u), bins=bins)[0]
        except AttributeError:
            spike_trains = numpy.histogram(ts, bins=bins)[0]

    return spike_trains
