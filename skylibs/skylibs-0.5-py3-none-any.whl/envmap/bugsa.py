from envmap import EnvironmentMap
import numpy as np
from matplotlib import pyplot as plt


height = 4
spheremapsize = (height*2, height*4)
e = EnvironmentMap(np.empty(spheremapsize), 'latlong')
x, y, z, valid = e.worldCoordinates()
sa = e.solidAngles()
plt.imshow(sa)
plt.colorbar()
plt.show()
