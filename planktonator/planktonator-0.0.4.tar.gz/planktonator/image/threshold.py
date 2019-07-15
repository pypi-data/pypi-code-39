from skimage.filters import rank
# from skimage.util import img_as_ubyte
from skimage.morphology import disk
import numpy as np

def otsu(img,radius = 15):
    '''
    Local Otsu
    '''
    local_otsu      = rank.otsu(np.rint(img).astype('uint8'),disk(radius))
    mask            = np.array(np.zeros(np.shape(img)))
    highidx         = img>=local_otsu
    lowidx          = img<local_otsu
    mask[highidx]   = 255
    mask[lowidx]    = 0
    return mask