import numpy as np

import joblib


img0 = np.random.random((1000,1000))

seg=256


im_shape = img0.shape
hh = int(math.ceil(im_shape[0]/seg))
ww = int(math.ceil(im_shape[1]/seg))

