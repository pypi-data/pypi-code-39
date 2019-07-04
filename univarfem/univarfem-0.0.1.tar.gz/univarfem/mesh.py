import numpy as np


class IntervalMesh:
    """ Finite element mesh for a univariate interval """
    def __init__(self, points):
        points = np.sort(points)

        self._points = points
        self._elements = np.column_stack((np.arange(0, self.npoints-1),
                                          np.arange(1, self.npoints)))

    @property
    def points(self):
        """ Points forming the mesh. """
        return self._points

    @property
    def elements(self):
        """ Indices of vertices for each element of the mesh. """
        return self._elements

    @property
    def boundary_nodes(self):
        """ Index of points on the boundary. """
        return [0, self.npoints-1]

    @property
    def npoints(self):
        """ Number of points in the mesh """
        return self.points.shape[0]

