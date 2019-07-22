"""
module for generating bravais lattices.
"""
import numpy as np
# pylint: disable=E0611
from scipy.spatial import cKDTree


def cells_function_factory(points, num_cell_vertices=7, boxsize=None):
    """
    Builds a function that takes a point and returns a candidate for
    The unit cell.
    """
    # Build a CDT with PBC
    kdt = cKDTree(points, boxsize=boxsize)

    def func(point):
        distance, index = kdt.query(point, num_cell_vertices)
        return distance, index

    return func


def create_lattice_vector(vector, angle):
    """
    Generates the component of a lattice vector given an angle.

    Args:
        vector (np.array): the first vector
        angle  (int): the angle in degrees.
    """
    radians = np.radians(angle)
    cos, sin = np.cos(radians), np.sin(radians)
    rotation_matrix = np.array([[cos, sin], [-sin, cos]])
    a_vec = np.array(vector)
    b_vec = np.dot(rotation_matrix, a_vec)
    return a_vec, b_vec


def create_lattice(shape, lattice_vectors, slicer=None, translate=None):
    """
    Generates a lattice given a shape and lattice vectors

    Args:
       shape (tuple): shape of the lattice in a grid of points
       lattice_vectors (np.array): a pair of lattice vectors
       slicer (func): takes a function that knows how to remove points from  the lattice.
       translate (func): function that knows how to shift the points to a new center
    """
    # Translate along one vector to fill up the bottom row.
    base = [(x*lattice_vectors[0][0], 0) for x in range(0, shape[0])]

    points = np.array([x*np.array(lattice_vectors[1]) +
                       base for x in range(0, shape[1])]).reshape(shape[0]*shape[1], 2)

    if translate is not None:
        points = translate(points)

    if slicer is not None:
        points = slicer(points)

    return points


def _centroid(points):
    """
    Finds the center of a bunch of points.

    Args:
        points (np.array): points of which we will find the center.
    """
    length = points.shape[0]
    sum_x = np.sum(points[:, 0])
    sum_y = np.sum(points[:, 1])
    return np.array([sum_x / length, sum_y / length])


def translation(new_center=np.array([0, 0])):
    """
    Translation wrapper
    """
    def func(points):
        """
        Shifts the centroid to a new center

        Args:
            points np.array(points): np array of points
            new_center (np.array): np.array representing the center.
        """
        center = _centroid(points)
        vec = new_center - center
        points = np.array([point+vec for point in points])
        return points
    return func


def rectangle_slicer(x_boundary, y_boundary):
    """
    Wrapper for methods using a square slicer.

    Args:
        length (tuple): a float representing the length
        width  (tuple): a float representing the width

    """

    def func(points):
        """
        Function to remove points outside the boundary.
        """
        # Remove points outside of the X boundary
        points = [point for point in points if point[0]
                  > x_boundary[0] and point[0] < x_boundary[1]]

        points = [point for point in points if point[1]
                  > y_boundary[0] and point[1] < y_boundary[1]]

        return np.array(points)

    return func


def radial_slicer(radius):
    """
    Wrapper for methods using a radial slicer.

    Args:
        radius (float): a float representing how far from the center to cut points
    """
    def func(points):
        """
        Function to remove points outside of a radius from the center

        Args:
            points (np.array): an array of points
        """
        center = _centroid(points)
        res = [point for point in points if np.linalg.norm(point-center) <= radius]
        return np.array(res)

    return func
