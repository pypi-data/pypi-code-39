"""
The main module of sslf (simple spectral line finder).
The provided Spectrum class is intended to facilitate all functionality.
"""

# Python 2 and 3 compatibility
from future.builtins import range
from future.utils import raise_with_traceback

import copy
import logging
import warnings

import numpy as np
import numpy.ma as ma
from scipy import signal


logger = logging.getLogger(__name__)


def find_background_rms(array, num_chunks, use_chunks):
    """
    In order to obtain a better estimate of a spectrum's RMS, break the input
    array into evenly sized chunks (or as even as possible), sort the chunks
    by RMS, then return the average of some of these chunks as the true RMS.

    Parameters
    ----------
    array : array_like
        The 1-dimensional spectrum we wish to determine the RMS for.

    num_chunks : int, optional
        Split `array` into this many chunks for RMS calculation.

    use_chunks : int, optional
        Use this many chunks from `array` for RMS calculation.
    """

    chunks = np.array_split(array, num_chunks)
    if isinstance(array, ma.core.MaskedArray):
        # The following requires np.errstate, because numpy.ma apparently throws
        # floating point errors erroneously.
        # https://github.com/numpy/numpy/issues/4895
        with np.errstate(under="ignore"):
            sorted_by_rms = sorted([np.std(x.data) for x in chunks])
    else:
        sorted_by_rms = sorted([np.std(x) for x in chunks])
    logger.debug("rms chunks = %s", sorted_by_rms)
    mean = np.mean(sorted_by_rms[:use_chunks])
    if mean == 0:
        raise_with_traceback(ValueError("RMS is 0, which cannot be used."))
    return mean


def _blank_spectrum_part(spectrum, channel_edges, value=0, spectrum_size=None):
    # Use the supplied spectrum_size, if available.
    if spectrum_size is None:
        spectrum_size = len(spectrum)

    lower = max([0, channel_edges[0]])
    upper = min([spectrum_size, channel_edges[1]])
    spectrum[lower:upper] = value


class SpectralLine(object):
    """
    A very simple object to track properties of a spectral line.

    namedtuple -> immutable.
    recordtype -> deprecated.
    namedlist -> no longer maintained.
    dataclasses -> python 3.7+
    What a language :)))
    """
    def __init__(self, c, s, ces):
        self.peak_channel = c
        self.peak_snr = s
        self.channel_edges = ces


class Spectrum(object):
    def __init__(self, spectrum, vel=None, num_chunks=5, use_chunks=3):
        """
        Provide a spectrum to find lines on, and/or remove the bandpass from.
        The optional vel parameter essentially provides an "x-axis" to the
        data, such that peak positions can be determined in terms of this
        axis rather than merely the channel position in the spectrum.
        Note that any NaN values in the spectrum are filtered.

        The noise RMS of `spectrum` is determined here, to provide it's value to
        the user, and ensure that its value is not zero. For this reason,
        adjusting `num_chunks` and `use_chunks` here is probably not important.

        Parameters
        ----------
        spectrum : array_like
            The 1-dimensional spectrum we will be performing line-finding on.

        vel : array_like, optional
            Supply an equally-sized array to `spectrum` to have `sslf` report
            the velocities (or some other arbitrary interpretation of the x-axis
            of `spectrum`) of found lines.

        num_chunks : int, optional
            When calculating the RMS of `spectrum`, break `spectrum` into
            equally-sized chunks according to `num_chunks`.

        use_chunks : int, optional
            When calculating the RMS of `spectrum`, use this many equally-sized
            chunks from when `spectrum` was split according to `num_chunks`.
        """

        # Ensure the sanity of types.
        if not isinstance(spectrum, (list, np.ndarray)):
            raise_with_traceback(ValueError("spectrum is not a list or numpy array ({}).".format(type(spectrum))))
        spectrum = np.array(spectrum)

        if vel is not None:
            if not isinstance(vel, (list, np.ndarray)):
                raise_with_traceback(ValueError("vel is not a list or numpy array ({}).".format(type(vel))))
            else:
                vel = np.array(vel)

        # Filter any NaNs, scipy doesn't like them.
        if np.any(np.isnan(spectrum)):
            nan_indices = np.isnan(spectrum)
            self.original = spectrum[~nan_indices]
            if vel is not None:
                self.vel = vel[~nan_indices]
            else:
                self.vel = None
        else:
            self.original = spectrum
            self.vel = vel

        self.rms = find_background_rms(spectrum, num_chunks=num_chunks, use_chunks=use_chunks)
        self.spectrum_length = self.original.size

    def find_cwt_peaks(self, scales, rms=None, snr=6.5, wavelet=signal.ricker,
                       num_chunks=5, use_chunks=3):
        """
        From the input spectrum (and a range of scales to search):
        - perform a continuous wavelet transformation (CWT)
        - find a significant peak in the CWT matrix
        - mask this peak in wavelet space, for all scales
        - loop from step 2, until no significant peaks remain
        - return the list of peaks

        In my experience, an SNR of 6.5 is a good compromise for reducing the number
        of false positives found while reliably finding real, significant peaks.

        It may be worthwhile to smooth the spectrum before performing the CWT.

        Parameters
        ----------
        scales : array_like
            The channel-widths to use when performing the CWT, and thus the
            channel-widths we use when searching for spectral lines.

        rms : float, optional
            Manually specify the noise RMS to use for line finding. Using this
            option means that `num_chunks` and `use_chunks` are not used.

        snr : float, optional
            The significance threshold of any found spectral line.

        wavelet : function
            The wavelet to use when performing the CWT. The wavelet used should
            have a similar profile to any spectral lines that are being
            searched.

        num_chunks : int, optional
            When calculating the RMS of a CWT slice, break the slice into
            equally-sized chunks according to `num_chunks`.

        use_chunks : int, optional
            When calculating the RMS of a CWT slice, use this many equally-sized
            chunks from when the slice was split according to `num_chunks`.
        """

        self.lines = []
        cwt_mat = signal.cwt(self.original, wavelet, scales)
        cwt_mat = ma.array(cwt_mat)

        while True:
            peak_pixel = cwt_mat.argmax()
            i, peak_channel = np.unravel_index(peak_pixel, cwt_mat.shape)
            peak = cwt_mat[i, peak_channel]
            if rms is not None:
                _rms = rms
            else:
                _rms = find_background_rms(cwt_mat[i], num_chunks=num_chunks, use_chunks=use_chunks)
            sig = peak / _rms
            logger.debug("Biggest peak at channel %s, scale %s, rms = %s",
                         peak_channel, scales[i], rms)

            # If this maximum is not significant, we're done.
            if sig < snr:
                logger.debug("Peak is not significant (%s < %s); finishing", sig, snr)
                break
            # Otherwise, blank this line across all scales.
            else:
                for j, s in enumerate(scales):
                    # If the line is too close to the edge,
                    # cap the mask at the edge.
                    lower = max([0, peak_channel - 2 * s])
                    upper = min([self.spectrum_length, peak_channel + 2 * s])
                    logger.debug("Blanked channels %s to %s (scale = %s)",
                                 lower, upper, s)
                    cwt_mat[j, lower:upper] = ma.masked
                self.lines.append(SpectralLine(peak_channel, sig, (peak_channel - scales[i],
                                                                   peak_channel + scales[i])))

        self.channel_peaks = [p.peak_channel for p in self.lines]
        self.peak_snrs = [p.peak_snr for p in self.lines]
        self.channel_edges = [p.channel_edges for p in self.lines]
        if self.vel is not None:
            self.vel_peaks = [self.vel[p.peak_channel] for p in self.lines]
        logger.debug("Channel peaks: %s", self.channel_peaks)
        logger.debug("Peak SNRs: %s", self.peak_snrs)
        logger.debug("Peak widths: %s", self.channel_edges)
        if self.vel is not None:
            logger.debug("Velocity peaks: %s", self.vel_peaks)

    def vel_peaks2chan_peaks(self):
        """
        This function is useful for when you know the velocities of the spectral lines,
        and need to determine the relevant channels before subtracting the bandpass.
        """
        self.channel_peaks = []
        for vp in self.vel_peaks:
            self.channel_peaks.append(np.abs(self.vel - vp).argmin())
        logger.debug("Channel peaks: %s", self.channel_peaks)

    def refine_line_widths(self, significance_cutoff=2.0, rms=None):
        """
        Use 'walkers' from each of the spectral line peaks to accurately find
        where the line ends in the noise. This is useful when the default,
        symmetric line widths found by the CWT aren't good enough.

        Parameters
        ----------
        significance_cutoff : float, optional
            When finding the edge of a spectral line's profile, use this
            signal-to-noise ratio to determine the cutoff.

        rms : float, optional
            Manually specify the noise RMS when finding profile edges. This
            simply affects the `significance_cutoff` * `rms` calculation. The
            default is the value determined by `find_background_rms` when the
            Spectrum object was created.
        """
        if rms is not None:
            _rms = rms
        else:
            _rms = self.rms

        depressed = self.original - significance_cutoff * _rms
        crossings = np.where(np.diff(np.sign(depressed)))[0]
        # If `crossings` is empty, then the RMS or self.original may be
        # ill-conditioned. Issue a warning and preserve the original edges.
        if crossings.size == 0:
            warnings.warn("Profile edges not found; RMS or spectrum may be ill-conditioned.",
                          UserWarning)
            return

        for line in self.lines:
            peak_crossings = crossings - line.peak_channel
            pks = peak_crossings.size
            negative_edge_index = np.where(peak_crossings < 0,
                                           peak_crossings,
                                           -np.inf).argmax()

            # Handle edges that meet the ends of the spectrum.
            if peak_crossings[negative_edge_index] >= 0:
                negative_edge = 0
            else:
                negative_edge = line.peak_channel + peak_crossings[negative_edge_index]

            if negative_edge_index + 1 == pks:
                positive_edge = self.spectrum_length - 1
            else:
                positive_edge = line.peak_channel + peak_crossings[negative_edge_index + 1]

            line.channel_edges = (negative_edge, positive_edge)

        self.channel_edges = [p.channel_edges for p in self.lines]

    def subtract_bandpass(self,
                          window_length=151,
                          poly_order=1,
                          allowable_peak_gap=10,
                          bandpass_func=None):
        """
        Flag the locations of any lines, and subtract the non-zero bandpass
        everywhere else. Provide the flattened spectrum in self.modified.

        If the spectral line widths are too large or too small, then they may
        be adjusted by iterating over the `peaks` attribute before calling this
        method.

        Parameters
        ----------
        window_length : int, optional
            The window_length to be used in scipy's savgol_filter. This should
            be bigger than the expected width of any spectral lines, but not
            so big that it is comparable to the length of the spectrum. In a
            sense, it specifies how far to look ahead and behind every channel
            when considering bandpass shape. If this is too small, it will
            behave more like a low-pass filter than a high-pass filter, when we
            probably want it to be more on the high-pass side.

        poly_order : int, optional
            The order of the polynomial fitting to be done over the spectral
            lines and with the savgol_filter. 1 (linear) is generally sensible,
            especially as higher orders are susceptible to Runge's phenomenon.

        allowable_peak_gap : int, optional
            The minimum number of channels between any two spectral lines before
            sslf considers them to be the same for the purposes of filtering.
            This avoids using noisy channels between lines for interpolation,
            and getting a poor subtraction. Currently disabled.

        bandpass_func : callable, optional
            If present, this specifies the function to use when determining a
            bandpass shape for subtraction. The default is
            lambda x: scipy.signal.savgol_filter(x,
                                                 window_length=window_length,
                                                 polyorder=poly_order)
        """

        mask = np.zeros_like(self.original)

        if bandpass_func is None:
            bandpass_func = lambda x: signal.savgol_filter(x,
                                                           window_length=window_length,
                                                           polyorder=poly_order)

        # Blank the spectrum containing spectral lines, so we can fit the
        # line-free bandpass around them.
        for ce in self.channel_edges:
            _blank_spectrum_part(mask, channel_edges=ce, value=1,
                                 spectrum_size=self.spectrum_length)

        self.filtered = copy.copy(self.original)

        # Find where lines start and end.
        edges = []
        if mask[0] == 1:
            edges.append(0)
        for e in np.where(np.diff(mask))[0]:
            edges.append(e)
        if mask[-1] == 1:
            edges.append(self.spectrum_length - 1)

        # Interpolate between gaps in the spectrum.
        for i in range(len(edges) // 2):
            e1, e2 = edges[2 * i], edges[2 * i + 1]
            logger.debug("Interpolation edges: %s, %s", e1, e2)

            # if e1 < allowable_peak_gap or e2 > self.spectrum_length - allowable_peak_gap:
            #     logger.debug("Interpolation edges are too close")
            #     continue
            # # Need a check for e2 being too close to the next e1.

            range_1 = np.arange(e1 - allowable_peak_gap, e1)
            range_2 = np.arange(e2, e2 + allowable_peak_gap)

            if np.any(range_1 <= 0):
                interp_range = [0] + range_2.tolist()
                values = [0] + self.filtered[range_2].tolist()
                poly_fit = np.poly1d(np.polyfit(interp_range, values, poly_order))
            elif np.any(range_2 >= self.spectrum_length - 1):
                interp_range = range_1.tolist() + [self.spectrum_length - 1]
                values = self.filtered[range_1].tolist() + [0]
                poly_fit = np.poly1d(np.polyfit(interp_range, values, poly_order))
            else:
                interp_range = range_1.tolist() + range_2.tolist()
                poly_fit = np.poly1d(np.polyfit(interp_range,
                                                self.filtered[interp_range],
                                                poly_order))
            self.filtered[e1:e2] = poly_fit(np.arange(e1, e2))

        self.bandpass = bandpass_func(self.filtered)
        self.modified = self.original - self.bandpass
