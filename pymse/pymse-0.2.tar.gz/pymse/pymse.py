import numpy as np


########################################################################
class PyMSE:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, data):
        """Constructor"""

        self.data = data
        self.data_cg = self.data.copy()

        self.mse = np.vectorize(self.sample_entropy)

    # ----------------------------------------------------------------------
    def coarse_grain(self, j):
        """"""
        data_cg = self.data.copy()
        for i in range(self.data.shape[0] // j):
            data_cg[i] = 0
            for k in range(0, j):
                data_cg[i] += self.data[i * j + k]
            data_cg[i] /= float(j)

        return data_cg

    # ----------------------------------------------------------------------
    def sample_entropy(self, scale=1, m=2, r=0.15):
        """"""

        std = np.std(self.data)
        data_cg = self.coarse_grain(scale)

        nlin = self.data.shape[0]
        nlin_j = (nlin // scale) - m
        r_new = r * std

        cont = np.zeros(m + 2)

        for i in range(nlin_j):
            for l in range(i + 1, nlin_j):

                k = 0
                while k < m and (np.abs(data_cg[i + k] - data_cg[l + k]) <= r_new):
                    k += 1
                    cont[k] += 1

                if k == m and (np.abs(data_cg[i + m] - data_cg[l + m]) <= r_new):
                    cont[m + 1] += 1

        if cont[m + 1] == 0 or cont[m] == 0:
            return -1 * np.log(1.0 / ((nlin_j) * (nlin_j - 1)))
        else:
            return -1 * np.log(float(cont[m + 1]) / cont[m])


# ----------------------------------------------------------------------
def mse(data, scale=range(1, 21), m=2, r=0.15):
    """"""

    pymse = PyMSE(data)
    scale = np.array(scale)
    if isinstance(m, (int, float)):
        m = [m]
    m = np.array(m)

    if isinstance(r, (int, float)):
        r = [r]
    r = np.array(r)

    return pymse.mse(scale, m[:, np.newaxis], r[:, np.newaxis, np.newaxis])


