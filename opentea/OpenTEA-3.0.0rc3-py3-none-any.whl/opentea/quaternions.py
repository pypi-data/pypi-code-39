#!/usr/bin/env python
"""
Quaternion utilities, for 3D rotaion around a directed axis
"""



from math import cos, sin, sqrt



def vect_normalize(v, tolerance=0.00001):
    """ mave unit vect
    v is a tuple
    """
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance:
        mag = sqrt(mag2)
        v = tuple(n / mag for n in v)
    return v


def tuple_plus(v1, v2):
    """ add tuples
    v1, v2 same dimension tuples
    ! need dimension check
    """
    res = tuple(a+b for a, b in list(zip(v1, v2)))
    return res


def tuple_minus(v1, v2):
    """ substract tuples
    v1, v2 same dimension tuples
    ! need dimension check
    """
    res = tuple(a-b for a, b in list(zip(v1, v2)))
    return res


def quat_mult(q1, q2):
    """ quaternion multiplication
    q1, q2 4D tuples
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z


def quat_conjugate(q):
    """ conjugate quaternion
    """
    q = vect_normalize(q)
    w, x, y, z = q
    return (w, -x, -y, -z)


def quatvect_mult(q1, v1):
    """ multiply quatertion
    """
    # v1 = vect_normalize(v1)
    q2 = (0.0, ) + v1
    return quat_mult(quat_mult(q1, q2), quat_conjugate(q1))[1:]


def axisangle_to_quat(v, theta):
    """ from axis and angle to quaternion
    v is a 3D tuple (direction)
    theta an angle
    ! need dimension check
    """
    v = vect_normalize(v)
    x, y, z = v
    theta /= 2
    w = cos(theta)
    x = x * sin(theta)
    y = y * sin(theta)
    z = z * sin(theta)
    return w, x, y, z
