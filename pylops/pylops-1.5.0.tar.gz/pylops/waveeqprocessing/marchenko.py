import logging
import warnings
import numpy as np

from scipy.signal import filtfilt
from scipy.sparse.linalg import lsqr
from scipy.special import hankel2
from pylops.utils import dottest as Dottest
from pylops import Diagonal, Identity, Block, BlockDiag, Roll
from pylops.waveeqprocessing.mdd import MDC

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)

def directwave(wav, trav, nt, dt, nfft=None):
    r"""Analytical direct wave

    Compute analytical 2d Green's function in frequency domain given
    a traveltime curve ``trav`` and wavelet ``wav``.

    Parameters
    ----------
    wav : :obj:`numpy.ndarray`
        Wavelet in time domain to apply to direct arrival when created
        using ``trav``. Phase will be discarded resulting in a zero-phase
        wavelet with same amplitude spectrum as provided by ``wav``
    trav : :obj:`numpy.ndarray`
        Traveltime of first arrival from subsurface point to
        surface receivers of size :math:`\lbrack nr \times 1 \rbrack`
    nt : :obj:`float`, optional
        Number of samples in time
    dt : :obj:`float`, optional
        Sampling in time
    nfft : :obj:`int`, optional
        Number of samples in fft time (if ``None``, :math:`nfft=nt`)

    Returns
    -------
    direct : :obj:`numpy.ndarray`
        Direct arrival in time domain of size
        :math:`\lbrack nt \times nr \rbrack`

    """
    nr = len(trav)
    nfft = nt if nfft is None or nfft < nt else nfft
    W = np.abs(np.fft.rfft(wav, nfft)) * dt
    f = 2 * np.pi * np.arange(nfft) / (dt * nfft)

    direct = np.zeros((nfft, nr), dtype=np.complex128)
    for it in range(len(W)):
        #direct[it] = W[it] * 1j * f[it] * np.exp(-1j * ((f[it] * trav) \
        #             + np.sign(f[it]) * np.pi / 4)) / \
        #             np.sqrt(8 * np.pi * np.abs(f[it]) * trav + 1e-10)
        direct[it] = W[it] * 1j * f[it] * (-1j) * \
                     hankel2(0, f[it] * trav + 1e-10) / 4

    direct = np.fft.irfft(direct, nfft, axis=0) / dt
    direct = np.real(direct[:nt])
    return direct


class Marchenko():
    r"""Marchenko redatuming

    Solve multi-dimensional Marchenko redatuming problem using
    :py:func:`scipy.sparse.linalg.lsqr` iterative solver.

    Parameters
    ----------
    R : :obj:`numpy.ndarray`
        Multi-dimensional reflection response in time or frequency
        domain of size :math:`[n_s \times n_r \times n_t/n_{fmax}]`
    R1 : :obj:`bool`, optional
        *Deprecated*, will be removed in v2.0.0. Simply kept for
        back-compatibility with previous implementation
    dt : :obj:`float`, optional
        Sampling of time integration axis
    nt : :obj:`float`, optional
        Number of samples in time (not required if ``R`` is in time)
    dr : :obj:`float`, optional
        Sampling of receiver integration axis
    nfmax : :obj:`int`, optional
        Index of max frequency to include in deconvolution process
    wav : :obj:`numpy.ndarray`, optional
        Wavelet to apply to direct arrival when created using ``trav``
    toff : :obj:`float`, optional
        Time-offset to apply to traveltime
    nsmooth : :obj:`int`, optional
        Number of samples of smoothing operator to apply to window
    dtype : :obj:`bool`, optional
        Type of elements in input array.
    saveRt : :obj:`bool`, optional
        Save ``R`` and ``R^H`` to speed up the computation of adjoint of
        :class:`pylops.signalprocessing.Fredholm1` (``True``) or create
        ``R^H`` on-the-fly (``False``) Note that ``saveRt=True`` will be
        faster but double the amount of required memory

    Attributes
    ----------
    ns : :obj:`int`
        Number of samples along source axis
    nr : :obj:`int`
        Number of samples along receiver axis
    shape : :obj:`tuple`
        Operator shape
    explicit : :obj:`bool`
        Operator contains a matrix that can be solved explicitly
        (True) or not (False)

    Raises
    ------
    TypeError
        If ``t`` is not :obj:`numpy.ndarray`.

    See Also
    --------
    MDC : Multi-dimensional convolution
    MDD : Multi-dimensional deconvolution

    Notes
    -----
    Marchenko redatuming is a method that allows to produce correct
    subsurface-to-surface responses given the availability of a
    reflection data and a macro-velocity model [1]_.

    The Marchenko equations can be written in a compact matrix
    form [2]_ and solved by means of iterative solvers such as LSQR:

    .. math::
        \begin{bmatrix}
           \Theta \mathbf{R} \mathbf{f_d^+}  \\
           \mathbf{0}
        \end{bmatrix} =
        \mathbf{I} -
        \begin{bmatrix}
           \mathbf{0}  &   \Theta \mathbf{R}   \\
           \Theta \mathbf{R^*} & \mathbf{0}
        \end{bmatrix}
        \begin{bmatrix}
           \mathbf{f^-}  \\
           \mathbf{f_m^+}
        \end{bmatrix}

    Finally the subsurface Green's functions can be obtained applying the
    following operator to the retrieved focusing functions

    .. math::
        \begin{bmatrix}
           -\mathbf{g^-}  \\
           \mathbf{g^{+ *}}
        \end{bmatrix} =
        \mathbf{I} -
        \begin{bmatrix}
           \mathbf{0}  &    \mathbf{R}   \\
           \mathbf{R^*} & \mathbf{0}
        \end{bmatrix}
        \begin{bmatrix}
           \mathbf{f^-}  \\
           \mathbf{f^+}
        \end{bmatrix}

    .. [1] Wapenaar, K., Thorbecke, J., Van der Neut, J., Broggini, F.,
        Slob, E., and Snieder, R., "Marchenko imaging", Geophysics, vol. 79,
        pp. WA39-WA57. 2014.

    .. [2] van der Neut, J., Vasconcelos, I., and Wapenaar, K. "On Green's
       function retrieval by iterative substitution of the coupled
       Marchenko equations", Geophysical Journal International, vol. 203,
       pp. 792-813. 2015.

    """
    def __init__(self, R, R1=None, dt=0.004, nt=None, dr=1.,
                 nfmax=None, wav=None, toff=0.0, nsmooth=10,
                 dtype='float64', saveRt=True):
        warnings.warn('A new implementation of Marchenko is provided in v1.5.0. '
                      'This currently affects only the inner working of the '
                      'operator, end-users can continue using the operator in '
                      'the same way. Nevertheless, R1 is not required anymore'
                      'even when R is provided in frequency domain. It is '
                      'recommended to start using the operator without the R1 '
                      'input as this behaviour will become default in '
                      'version v2.0.0 and R1 will be removed from the inputs.',
                      FutureWarning)
        # Save inputs into class
        self.dt = dt
        self.dr = dr
        self.wav = wav
        self.toff = toff
        self.nsmooth = nsmooth
        self.saveRt = saveRt
        self.dtype = dtype
        self.explicit = False

        # Infer dimensions of R
        if not np.iscomplexobj(R):
            self.ns, self.nr, self.nt = R.shape
            self.nfmax = nfmax
        else:
            self.ns, self.nr, self.nfmax = R.shape
            self.nt = nt
            if nt is None:
                logging.error('nt must be provided as R is in frequency')
        self.nt2 = int(2*self.nt-1)
        self.t = np.arange(self.nt)*self.dt

        # Fix nfmax to be at maximum equal to half of the size of fft samples
        if self.nfmax is None or self.nfmax > np.ceil((self.nt2 + 1) / 2):
            self.nfmax = int(np.ceil((self.nt2+1)/2))
            logging.warning('nfmax set equal to (nt+1)/2=%d', self.nfmax)

        # Add negative time to reflection data and convert to frequency
        if not np.iscomplexobj(R):
            Rtwosided = np.concatenate((np.zeros((self.ns, self.nr,
                                                  self.nt - 1)), R), axis=-1)
            Rtwosided_fft = np.fft.rfft(Rtwosided, self.nt2,
                                        axis=-1) / np.sqrt(self.nt2)
            self.Rtwosided_fft = Rtwosided_fft[..., :nfmax]
        else:
            self.Rtwosided_fft = R
        # bring frequency to first dimension
        self.Rtwosided_fft = self.Rtwosided_fft.transpose(2, 0, 1)

    def apply_onepoint(self, trav, G0=None, nfft=None, rtm=False, greens=False,
                       dottest=False, fast=None, **kwargs_lsqr):
        r"""Marchenko redatuming for one point

        Solve the Marchenko redatuming inverse problem for a single point
        given its direct arrival traveltime curve (``trav``)
        and waveform (``G0``).

        Parameters
        ----------
        trav : :obj:`numpy.ndarray`
            Traveltime of first arrival from subsurface point to
            surface receivers of size :math:`[n_r \times 1]`
        G0 : :obj:`numpy.ndarray`, optional
            Direct arrival in time domain of size :math:`[n_r \times n_t]`
            (if None, create arrival using ``trav``)
        nfft : :obj:`int`, optional
            Number of samples in fft when creating the analytical direct wave
        rtm : :obj:`bool`, optional
            Compute and return rtm redatuming
        greens : :obj:`bool`, optional
            Compute and return Green's functions
        dottest : :obj:`bool`, optional
            Apply dot-test
        fast : :obj:`bool`
            *Deprecated*, will be removed in v2.0.0
        **kwargs_lsqr
            Arbitrary keyword arguments for
            :py:func:`scipy.sparse.linalg.lsqr` solver

        Returns
        ----------
        f1_inv_minus : :obj:`numpy.ndarray`
            Inverted upgoing focusing function of size :math:`[n_r \times n_t]`
        f1_inv_plus : :obj:`numpy.ndarray`
            Inverted downgoing focusing function
            of size :math:`[n_r \times n_t]`
        p0_minus : :obj:`numpy.ndarray`
            Single-scattering standard redatuming upgoing Green's function of
            size :math:`[n_r \times n_t]`
        g_inv_minus : :obj:`numpy.ndarray`
            Inverted upgoing Green's function of size :math:`[n_r \times n_t]`
        g_inv_plus : :obj:`numpy.ndarray`
            Inverted downgoing Green's function
            of size :math:`[n_r \times n_t]`

        """
        # Create window
        trav_off = trav - self.toff
        trav_off = np.round(trav_off / self.dt).astype(np.int)

        # window
        w = np.zeros((self.nr, self.nt))
        for ir in range(self.nr):
            w[ir, :trav_off[ir]] = 1
        w = np.hstack((np.fliplr(w), w[:, 1:]))
        if self.nsmooth > 0:
            smooth = np.ones(self.nsmooth) / self.nsmooth
            w = filtfilt(smooth, 1, w)

        # Create operators
        Rop = MDC(self.Rtwosided_fft, self.nt2, nv=1, dt=self.dt, dr=self.dr,
                  twosided=True, conj=False, transpose=False,
                  saveGt=self.saveRt, dtype=self.dtype)
        R1op = MDC(self.Rtwosided_fft, self.nt2, nv=1, dt=self.dt, dr=self.dr,
                   twosided=True, conj=True, transpose=False,
                   saveGt=self.saveRt, dtype=self.dtype)
        Rollop = Roll(self.nt2 * self.ns,
                      dims=(self.nt2, self.ns),
                      dir=0, shift=-1, dtype=self.dtype)
        Wop = Diagonal(w.T.flatten())
        Iop = Identity(self.nr * self.nt2)
        Mop = Block([[Iop, -1 * Wop * Rop],
                     [-1 * Wop * Rollop * R1op, Iop]]) * BlockDiag([Wop, Wop])
        Gop = Block([[Iop, -1 * Rop],
                     [-1 * Rollop * R1op, Iop]])

        if dottest:
            Dottest(Gop, 2 * self.ns * self.nt2,
                    2 * self.nr * self.nt2,
                    raiseerror=True, verb=True)
        if dottest:
            Dottest(Mop, 2 * self.ns * self.nt2,
                    2 * self.nr * self.nt2,
                    raiseerror=True, verb=True)

        # Create input focusing function
        if G0 is None:
            if self.wav is not None and nfft is not None:
                G0 = (directwave(self.wav, trav, self.nt,
                                 self.dt, nfft=nfft)).T
            else:
                logging.error('wav and/or nfft are not provided. '
                              'Provide either G0 or wav and nfft...')
                raise ValueError('wav and/or nfft are not provided. '
                                 'Provide either G0 or wav and nfft...')

        fd_plus = np.concatenate((np.fliplr(G0).T,
                                  np.zeros((self.nt - 1, self.nr))))

        # Run standard redatuming as benchmark
        if rtm:
            p0_minus = Rop * fd_plus.flatten()
            p0_minus = p0_minus.reshape(self.nt2, self.ns).T

        # Create data and inverse focusing functions
        d = Wop * Rop * fd_plus.flatten()
        d = np.concatenate((d.reshape(self.nt2, self.ns),
                            np.zeros((self.nt2, self.ns))))

        # Invert for focusing functions
        f1_inv = lsqr(Mop, d.flatten(), **kwargs_lsqr)[0]
        f1_inv = f1_inv.reshape(2 * self.nt2, self.nr)
        f1_inv_tot = f1_inv + np.concatenate((np.zeros((self.nt2, self.nr)),
                                              fd_plus))
        f1_inv_minus = f1_inv_tot[:self.nt2].T
        f1_inv_plus = f1_inv_tot[self.nt2:].T
        if greens:
            # Create Green's functions
            g_inv = Gop * f1_inv_tot.flatten()
            g_inv = np.real(g_inv) # cast to real as Gop is a complex operator
            g_inv = g_inv.reshape(2 * self.nt2, self.ns)
            g_inv_minus, g_inv_plus = -g_inv[:self.nt2].T, \
                                      np.fliplr(g_inv[self.nt2:].T)
        if rtm and greens:
            return f1_inv_minus, f1_inv_plus, p0_minus, g_inv_minus, g_inv_plus
        elif rtm:
            return f1_inv_minus, f1_inv_plus, p0_minus
        elif greens:
            return f1_inv_minus, f1_inv_plus, g_inv_minus, g_inv_plus
        else:
            return f1_inv_minus, f1_inv_plus

    def apply_multiplepoints(self, trav, G0=None, nfft=None,
                             rtm=False, greens=False,
                             dottest=False, **kwargs_lsqr):
        r"""Marchenko redatuming for multiple points

        Solve the Marchenko redatuming inverse problem for multiple
        points given their direct arrival traveltime curves (``trav``)
        and waveforms (``G0``).

        Parameters
        ----------
        trav : :obj:`numpy.ndarray`
            Traveltime of first arrival from subsurface points to
            surface receivers of size :math:`[n_r \times n_{vs}]`
        G0 : :obj:`numpy.ndarray`, optional
            Direct arrival in time domain of size
            :math:`[n_r \times n_{vs} \times n_t]` (if None, create arrival
            using ``trav``)
        nfft : :obj:`int`, optional
            Number of samples in fft when creating the analytical direct wave
        rtm : :obj:`bool`, optional
            Compute and return rtm redatuming
        greens : :obj:`bool`, optional
            Compute and return Green's functions
        dottest : :obj:`bool`, optional
            Apply dot-test
        **kwargs_lsqr
            Arbitrary keyword arguments
            for :py:func:`scipy.sparse.linalg.lsqr` solver

        Returns
        ----------
        f1_inv_minus : :obj:`numpy.ndarray`
            Inverted upgoing focusing function of size
            :math:`[n_r \times n_{vs} \times n_t]`
        f1_inv_plus : :obj:`numpy.ndarray`
            Inverted downgoing focusing functionof size
            :math:`[n_r \times n_{vs} \times n_t]`
        p0_minus : :obj:`numpy.ndarray`
            Single-scattering standard redatuming upgoing Green's function
            of size :math:`[n_r \times n_{vs} \times n_t]`
        g_inv_minus : :obj:`numpy.ndarray`
            Inverted upgoing Green's function of size
            :math:`[n_r \times n_{vs} \times n_t]`
        g_inv_plus : :obj:`numpy.ndarray`
            Inverted downgoing Green's function of size
            :math:`[n_r \times n_{vs} \times n_t]`

        """
        nvs = trav.shape[1]

        # Create window
        trav_off = trav - self.toff
        trav_off = np.round(trav_off / self.dt).astype(np.int)

        w = np.zeros((self.nr, nvs, self.nt))
        for ir in range(self.nr):
            for ivs in range(nvs):
                w[ir, ivs, :trav_off[ir, ivs]] = 1
        w = np.concatenate((np.flip(w, axis=-1), w[:, :, 1:]), axis=-1)
        if self.nsmooth > 0:
            smooth = np.ones(self.nsmooth) / self.nsmooth
            w = filtfilt(smooth, 1, w)

        # Create operators
        Rop = MDC(self.Rtwosided_fft, self.nt2, nv=nvs,
                  dt=self.dt, dr=self.dr, twosided=True,
                  conj=False, transpose=False, dtype=self.dtype)
        R1op = MDC(self.Rtwosided_fft, self.nt2, nv=nvs,
                   dt=self.dt, dr=self.dr, twosided=True,
                   conj=True, transpose=False, dtype=self.dtype)
        Rollop = Roll(self.ns * nvs * self.nt2,
                      dims=(self.nt2, self.ns, nvs),
                      dir=0, shift=-1, dtype=self.dtype)
        Wop = Diagonal(w.transpose(2, 0, 1).flatten())
        Iop = Identity(self.nr * nvs * self.nt2)
        Mop = Block([[Iop, -1 * Wop * Rop],
                     [-1 * Wop * Rollop * R1op, Iop]]) * BlockDiag([Wop, Wop])
        Gop = Block([[Iop, -1 * Rop],
                     [-1 * Rollop * R1op, Iop]])

        if dottest:
            Dottest(Gop, 2 * self.nr * nvs * self.nt2,
                    2 * self.nr * nvs * self.nt2,
                    raiseerror=True, verb=True)
        if dottest:
            Dottest(Mop, 2 * self.ns * nvs * self.nt2,
                    2 * self.nr * nvs * self.nt2,
                    raiseerror=True, verb=True)

        # Create input focusing function
        if G0 is None:
            if self.wav is not None and nfft is not None:
                G0 = np.zeros((self.nr, nvs, self.nt))
                for ivs in range(nvs):
                    G0[:, ivs] = (directwave(self.wav, trav[:, ivs],
                                             self.nt, self.dt, nfft=nfft)).T
            else:
                logging.error('wav and/or nfft are not provided. '
                              'Provide either G0 or wav and nfft...')
                raise ValueError('wav and/or nfft are not provided. '
                                 'Provide either G0 or wav and nfft...')

        fd_plus = np.concatenate((np.flip(G0, axis=-1).transpose(2, 0, 1),
                                  np.zeros((self.nt - 1, self.nr, nvs))))

        # Run standard redatuming as benchmark
        if rtm:
            p0_minus = Rop * fd_plus.flatten()
            p0_minus = p0_minus.reshape(self.nt2, self.ns,
                                        nvs).transpose(1, 2, 0)

        # Create data and inverse focusing functions
        d = Wop * Rop * fd_plus.flatten()
        d = np.concatenate((d.reshape(self.nt2, self.ns, nvs),
                            np.zeros((self.nt2, self.ns, nvs))))

        # Invert for focusing functions
        f1_inv = lsqr(Mop, d.flatten(), **kwargs_lsqr)[0]
        f1_inv = f1_inv.reshape(2 * self.nt2, self.nr, nvs)
        f1_inv_tot = \
            f1_inv + np.concatenate((np.zeros((self.nt2, self.nr, nvs)),
                                     fd_plus))
        f1_inv_minus = f1_inv_tot[:self.nt2].transpose(1, 2, 0)
        f1_inv_plus = f1_inv_tot[self.nt2:].transpose(1, 2, 0)

        if greens:
            # Create Green's functions
            g_inv = Gop * f1_inv_tot.flatten()
            g_inv = np.real(g_inv) # cast to real as Gop is a complex operator
            g_inv = g_inv.reshape(2 * self.nt2, self.ns, nvs)
            g_inv_minus = -g_inv[:self.nt2].transpose(1, 2, 0)
            g_inv_plus = np.flip(g_inv[self.nt2:], axis=0).transpose(1, 2, 0)

        if rtm and greens:
            return f1_inv_minus, f1_inv_plus, p0_minus, g_inv_minus, g_inv_plus
        elif rtm:
            return f1_inv_minus, f1_inv_plus, p0_minus
        elif greens:
            return f1_inv_minus, f1_inv_plus, g_inv_minus, g_inv_plus
        else:
            return f1_inv_minus, f1_inv_plus
