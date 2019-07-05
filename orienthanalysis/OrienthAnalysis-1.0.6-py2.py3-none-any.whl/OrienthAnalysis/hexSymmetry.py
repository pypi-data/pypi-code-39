
'''
THis function find 1/12 symmetric pin for an certain pin define by 2d array.
'''

import math
from scipy.linalg import solve
import numpy as np

def hexSym12(r:tuple, scale:int) -> tuple:
    '''
    :param r: coordination of one pin
    :param scale:
    :return: symmetric pin coord.
    '''

    if len(r) != 2: raise Exception("first parameter must be of length 2.")

    dx = 1                                                           # spacing of x axis
    dy = math.sqrt(3) / 2                                               # spacing of y axis
    center = (int(scale/2), int(scale/2))                            # coor. of the center pin
    rCrct = list(reversed( [r[0] - center[0], r[1] - center[1]] ))   # r corrected and reversed according to opposite
                                                                     # notion of (x, y) and (i,j)
    coor = (rCrct[0]*dx + rCrct[1]*dx/2, rCrct[1]*dy)
    print(rCrct, coor, center)
    lsym = (0, 1, 0)
    a, b, c = lsym
    x1, y1 = coor
    if a == 0:
        c2 = (x1, -2*c/b - y1)
    elif b == 0:
        c2 = (-2*c/a -x1, y1)
    else:
        A = np.array([[a/b, 1], [-b/a, 1]])
        Y = np.array([-2*c/b - y1 - a/b*x1, y1 - b/a*x1])
        c2 = solve(A, Y)

    x2, y2 = c2
    j2 = y2/dy
    i2 = (x2 - j2*dx/2)/dx
    print(i2, j2)
    r2 = i2 + center[0], j2 + center[1]
    return tuple(reversed(r2))

if __name__ == '__main__':
    r = (0,60)
    print(hexSym12(r,61))
