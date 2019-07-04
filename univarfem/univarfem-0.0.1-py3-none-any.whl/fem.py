import numpy as np
from .gaussquad import (IntervalGaussianQuadrature,
                        RectangleGaussianQuadrature)


class FEMSolver:
    """ Base FEM solver class. """
    def __init__(self, mesh):
        self._mesh = mesh

    @property
    def mesh(self):
        """ Mesh on which to solve the problem. """
        return self._mesh


class PoissonFEMSolver(FEMSolver):
    """ Solves the one dimensional Poisson problem using FEM. """
    def __init__(self, mesh, source):
        super(PoissonFEMSolver, self).__init__(mesh)

        self._source = source

    def assemble(self):
        """ Constructs the stiffness and load vector. """
        A = np.zeros((self.mesh.npoints, self.mesh.npoints))
        f = np.zeros(self.mesh.npoints)

        gaussquad = IntervalGaussianQuadrature(degree=2)

        for k, con_mat_row in enumerate(self.mesh.elements):
            x0, x1 = self.mesh.points[con_mat_row]

            # local basis functions
            psi = [lambda x: (x1 - x)/(x1-x0),
                   lambda x: (x - x0)/(x1-x0)]

            for i in range(2):
                for j in range(2):

                    Akij = (-1)**(1+(i==j)) / abs(x1-x0)

                    A[con_mat_row[i], con_mat_row[j]] += Akij

                # multiply the source by the local basis function
                def fpsi(x):
                    return self.source(x)*psi[i](x)

                f[con_mat_row[i]] += gaussquad.integrate(fpsi, x0, x1)

        # apply Essential boundary conditions
        A[self.mesh.boundary_nodes, :] = 0
        A[:, self.mesh.boundary_nodes] = 0
        A[self.mesh.boundary_nodes, self.mesh.boundary_nodes] = 1.

        f[self.mesh.boundary_nodes] = 0

        return A, f

    @property
    def source(self):
        """ Source function of the Poisson equation. """
        return self._source


class EllipticFEMSolver(FEMSolver):
    def __init__(self, mesh, coeff, source):
        super(EllipticFEMSolver, self).__init__(mesh)
        self._coeff = coeff
        self._source = source

    @property
    def source(self):
        """ Source function of the Poisson equation. """
        return self._source

    @property
    def coeff(self):
        """ Coefficient function of the elliptic PDE """
        return self._coeff

    def assemble(self):
        """ Constructs the stiffness and load vector. """
        A = np.zeros((self.mesh.npoints, self.mesh.npoints))
        f = np.zeros(self.mesh.npoints)

        int_gaussquad = IntervalGaussianQuadrature(degree=3)

        for k, con_mat_row in enumerate(self.mesh.elements):
            x0, x1 = self.mesh.points[con_mat_row]

            # local basis functions
            psi = [lambda x: (x1 - x)/(x1-x0),
                   lambda x: (x - x0)/(x1-x0)]

            # gradients of local basis functions
            psi_grad = [lambda x: -1/(x1-x0),
                        lambda x: 1/(x1-x0)]

            def weakform_integrand(x, i, j):
                return self.coeff(x) * psi_grad[i](x) * psi_grad[j](x)

            for i in range(2):
                for j in range(2):

                    akij = int_gaussquad.integrate(
                        lambda x: weakform_integrand(x, i, j), x0, x1)

                    A[con_mat_row[i], con_mat_row[j]] += akij

                # multiply the source by the local basis function
                def fpsi(x):
                    return self.source(x)*psi[i](x)

                f[con_mat_row[i]] += int_gaussquad.integrate(fpsi, x0, x1)

        # apply Essential boundary conditions
        A[self.mesh.boundary_nodes, :] = 0
        A[:, self.mesh.boundary_nodes] = 0
        A[self.mesh.boundary_nodes, self.mesh.boundary_nodes] = 1.

        f[self.mesh.boundary_nodes] = 0

        return A, f
