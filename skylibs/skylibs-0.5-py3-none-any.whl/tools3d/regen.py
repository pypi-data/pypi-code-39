import numpy as np
from envmap import EnvironmentMap
from pyshtools.shtools import SHExpandDH, MakeGridDH

from spharm import FSHT, iFSHT, sphericalHarmonicTransform, inverseSphericalHarmonicTransform



if __name__ == '__main__':
    from matplotlib import pyplot as plt

    for i in range(66):
        coeffs = np.zeros((2, 11, 11))
        coeffs_fsht = np.zeros((66, 1))

        coeffs_fsht[i, 0] = 1

        row = ((np.sqrt(8*i+1) - 1) / 2).astype('int32')
        coeffs[0, row, (i - (row*(row+1)//2))] = 1
        print(row, i - row**2)

        topo_rec = MakeGridDH(coeffs, lmax=31, sampling=2, lmax_calc=10)

        #db_coef = int((2*(degrees + 1)+1)**2/8)
        er_fsht = iFSHT(coeffs_fsht, 64)

        print(topo_rec.shape)
        print(er_fsht.data.shape)

        plt.clf()
        plt.subplot(131); plt.imshow(topo_rec); plt.colorbar()
        plt.subplot(132); plt.imshow(er_fsht.data[:,:,0]); plt.colorbar()
        plt.subplot(133); plt.imshow(topo_rec / er_fsht.data[:,:,0]); plt.clim([0.5, 5]); plt.colorbar()
        plt.show(block=False)
        plt.pause(1)

        print(np.nanmedian((topo_rec / er_fsht.data[:,:,0])))

        import pdb; pdb.set_trace()

