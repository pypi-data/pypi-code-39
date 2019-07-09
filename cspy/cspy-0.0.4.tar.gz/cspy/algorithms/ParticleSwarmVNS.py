"""
Copied and edited from https://github.com/100/Solid
"""

from abc import ABCMeta, abstractmethod
from math import sqrt
from random import random
from numpy import (apply_along_axis, argmin, array, copy, diag_indices_from,
                   dot, zeros)
from numpy.random import uniform


class ParticleSwarmVNS:
    """
    Conducts particle swarm optimization
    """

    __metaclass__ = ABCMeta

    def __init__(self, swarm_size, member_size, neighbourhood_size, lower_bound,
                 upper_bound, c1, c2, c3, max_iter, max_localiter):
        # Inputs
        self.swarm_size = swarm_size
        self.member_size = member_size
        self.hood_size = neighbourhood_size
        self.lower_bound = array([float(x) for x in lower_bound])
        self.upper_bound = array([float(x) for x in upper_bound])
        self.c1 = float(c1)
        self.c2 = float(c2)
        self.c3 = float(c3)
        self.max_iter = max_iter
        self.max_localiter = max_localiter
        # PSO Specific Parameters
        self.iter = 0
        self.pos = None
        self.vel = None
        self.best = None
        self.curr_obj = None
        self.global_best = None
        # VNS Specific Parameters
        self.local_best = None

    def __str__(self):
        return ('CURRENT STEPS: %d \n' +
                'BEST FITNESS: %f \n' +
                'BEST MEMBER: %s \n\n') % \
               (self.iter, self.curr_obj, str(self.global_best[0]))

    def __repr__(self):
        return self.__str__()

    def _init_swarm(self):
        """
        Initialises the variables that are altered during the algorithm

        :return: None
        """
        self.pos = uniform(self.lower_bound,
                           self.upper_bound,
                           size=(self.swarm_size, self.member_size))
        self.vel = uniform(self.lower_bound - self.upper_bound,
                           self.upper_bound - self.lower_bound,
                           size=(self.swarm_size, self.member_size))
        self.scores = self._score(self.pos)
        self.best = copy(self.pos)
        self._global_best()
        self.local_best = copy(self.pos[:self.hood_size])

    @abstractmethod
    def _objective(self, member):
        """
        Returns objective function value for a member of swarm -
        operates on 1D numpy array

        :param member: a member
        :return: objective function value of member
        """
        pass

    def _score(self, pos):
        """
        Applies objective function to all members of swarm

        :param pos: position matrix
        :return: score vector
        """
        return apply_along_axis(self._objective, 1, pos)

    def _best(self, old, new):
        """
        Finds the best objective function values for each member of swarm

        :param old: old values
        :param new: new values
        """
        old_scores = self._score(old)
        new_scores = self._score(new)
        best = []
        for i in range(len(old_scores)):
            if old_scores[i] < new_scores[i]:
                best.append(old[i])
            else:
                best.append(new[i])
        self.best = array(best)

    def _global_best(self):
        """
        Finds the global best across swarm
        """
        if self.global_best is None:
            self.global_best = array([self.pos[argmin(self.scores)]] *
                                     self.swarm_size)
            self.curr_obj = min(self.scores)

    @abstractmethod
    def _local_best(self, i):
        """
        Find local best using neighourhood size

        :param i: current iteration number
        """
        pass

    @abstractmethod
    def _VNS(self):
        pass

    def _run(self, verbose=True):
        """
        Conducts particle swarm optimization

        :param verbose: indicates whether or not to print progress regularly
        """
        self._init_swarm()
        while self.iter < self.max_iter:
            if verbose and ((self.iter) % 100 == 0):
                print(self)

            vel_new = self._get_vel_new()
            pos_new = self.pos + vel_new

            self._best(self.pos, pos_new)
            self.pos = pos_new
            # self._VNS(self.pos)
            self.scores = self._score(self.pos)
            self._global_best()
            self._local_best(self.iter)
            self.iter += 1
        if verbose:
            print("TERMINATING - REACHED MAXIMUM STEPS")
        return
        # self.global_best[0], self._objective(self.global_best[0])

    def _get_vel_new(self):
        # Generate random numbers
        u1 = zeros((self.swarm_size, self.swarm_size))
        u1[diag_indices_from(u1)] = [random() for _ in range(self.swarm_size)]
        u2 = zeros((self.swarm_size, self.swarm_size))
        u2[diag_indices_from(u2)] = [random() for _ in range(self.swarm_size)]
        u3 = zeros((self.hood_size, self.hood_size))
        u3[diag_indices_from(u3)] = [random() for _ in range(self.hood_size)]
        # Coefficients
        c = self.c1 + self.c2 + self.c3
        chi_1 = 2 / abs(2 - c - sqrt(pow(c, 2) - 4 * c))
        # Returns velocity
        return (chi_1 * (self.vel + (self.c1 * dot(u1,
                                                   (self.best - self.pos)))) +
                (self.c2 * dot(u2, (self.global_best - self.pos))) +
                (self.c3 * dot(u3, (self.local_best - self.pos))))

    #######
    # VNS #
    #######
    # Variable Neighbourhood search and related functions
    def _VNS(self, pos):
        it = 0  # local iteration counter
        while it < self.max_localiter:
            # Init candidate solution
            vel_new = self._local_S2(pos)
            pos_new = pos + vel_new
            self._best(pos, pos_new)
            it += 1
        self.pos = self.best

    def _local_S1(self, pos):
        u1 = zeros((self.swarm_size, self.swarm_size))
        u1[diag_indices_from(u1)] = [random() for _ in range(self.swarm_size)]
        # Returns velocity
        return dot(u1, pos)

    def _local_S2(self, pos):
        u1 = zeros((self.swarm_size, self.swarm_size))
        u1[diag_indices_from(u1)] = [random() for _ in range(self.swarm_size)]
        u2 = zeros((self.swarm_size, self.swarm_size))
        u2[diag_indices_from(u1)] = [random() for _ in range(self.swarm_size)]
        # Returns velocity
        return dot(u1, self.global_best) + dot(u2, pos)

    # def _inverse_discretise(self, path, rand):
    #     # print("HERE")
    #     nodes = self._sort_nodes(list(self.G.nodes()))
    #     nodes_indicator = zeros(len(nodes))
    #     sig = self.sig
    #     for i in range(len(nodes)):
    #         if nodes[i] in path:
    #             nodes_indicator[i] = 1
    #         else:
    #             sig[i] = rand
    #     return -log(1 / sig - 1)