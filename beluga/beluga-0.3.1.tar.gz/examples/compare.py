import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

sparse = np.load('sparse.npy')
dense = np.load('dense.npy')

plt.loglog(sparse[0,:], sparse[1,:], color='b', label='Sparse')
plt.loglog(dense[0,:], dense[1,:], color='r', label='Dense')
plt.xlabel('Arcs')
plt.ylabel('Time to Solution [s]')
plt.grid(True)
plt.legend()
plt.show()
