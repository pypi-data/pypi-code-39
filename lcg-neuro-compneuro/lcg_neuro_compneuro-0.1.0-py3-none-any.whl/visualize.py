"""
"""

import numpy as np
import warnings

try:
    import matplotlib.pyplot as plt

    def plotSpikes(ts, rho, color=(0, 0, 0, 0.15), axes=None):
        r"""Plots spikes in trials as vertical gray segments.

        Parameters
        ----------
        ts: float
            Time resolution of samples (in milliseconds), *i.e* :math:`\Delta t`.

        rho: :class:`numpy.ndarray`
            An (M, N) or (,N) array of M trials containing N-slot spike-trains each.

        color: tuple
            RGBA color of vertical bars. Low alpha values allow for better visualization when N is large.

        axes: :class:`matplotlib.axes.Axes`, optional
            Spikes are plotted onto the given axes object, if any, or to the current active axes object in the
            :mod:`matplotlib.pyplot` module, if ``axes`` is ``None``.
        """
        rho = np.array(rho)

        # Ensure rho is a 2D array
        n = rho.shape[-1]
        rho = rho.reshape((-1, n))
        m, n = rho.shape

        if axes is None:
            axes = plt

        for i in range(m):
            for j in range(n):
                if rho[i, j]:
                    axes.axvline(
                        x=j * ts,
                        ymin=i / m,
                        ymax=(i + 1) / m,
                        color=(0, 0, 0, 0.2),
                        linewidth=1.25,
                    )

        axes.xlim(0, n * ts)

    def plotTrial(ts, stim, rho):
        """Plots stimulus and spike train in a single trial.

        Parameters
        ----------
        stim: :class:`numpy.ndarray`
            An (,N) array of stimulus samples in a single trial.

        rho: :class:`numpy.ndarray`
            An (,N) spike-train array in a single trial.
        """
        stim = np.array(stim)
        rho = np.array(rho)

        if stim.shape != rho.shape:
            raise ValueError(
                "Stimulus and spike-train have different dimensions: %r vs. %r"
                % (stim, rho)
            )

        time = ts * np.arange(stim.shape[0], dtype=np.float)

        plotSpikes(ts, np.array([rho]))

        plt.plot(time, stim, label="Stimulus")
        plt.xlabel("Trial time (ms)")
        plt.ylabel("Stimulus")  # TODO: allow to parameterize stimulus units label


except ImportError as error:
    message = "\n".join(
        [
            "Could not import matplotlib.pyplot, so v2.visualize methods are not available.",
            "Original error: " + str(error),
        ]
    )
    warnings.warn(message, ImportWarning)
