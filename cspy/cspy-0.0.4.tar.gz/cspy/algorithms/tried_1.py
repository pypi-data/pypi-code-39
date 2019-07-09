from __future__ import absolute_import
from __future__ import print_function


import logging
# from time import sleep
from math import exp
from random import random
from networkx import has_path
from itertools import permutations
from algorithms.ParticleSwarm import ParticleSwarm
from numpy import zeros, vectorize, array
from preprocessing import check

log = logging.getLogger(__name__)


class StandardGraph:

    def __init__(self, G, max_res, min_res):
        # Check input graph and parameters
        check(G, max_res, min_res)
        # Input parameters
        self.G = G
        self.max_res = max_res
        self.min_res = min_res


class PSOLGENT(StandardGraph, ParticleSwarm):
    """
    Particle Swarm Optimization with combined Local and Global Expanding
    Neighborhood Topology (PSOLGENT) algorithm for the (resource)
    constrained shortest path problem (`Marinakis et al. 2017`_).

    Parameters
    ----------
    G : object instance :class:`nx.Digraph()`
        must have ``n_res`` graph attribute and all edges must have
        ``res_cost`` attribute.

    max_res : list of floats
        :math:`[H_F, M_1, M_2, ..., M_{n\_res}]` upper bounds for resource
        usage (including initial forward stopping point).
        We must have ``len(max_res)`` :math:`\geq 2`

    min_res : list of floats
        :math:`[H_B, L_1, L_2, ..., L_{n\_res}]` lower bounds for resource
        usage (including initial backward stopping point).
        We must have ``len(min_res)`` :math:`=` ``len(max_res)`` :math:`\geq 2`

    Returns
    -------
    path : list
        nodes in shortest path obtained.

    Raises
    ------
    Exception
        if no resource feasible path is found

    Notes
    -----
    The input graph must have a ``n_res`` attribute in the input graph has
    to be :math:`\geq 2`. The edges in the graph must all have a `res_cost`
    attribute.

    Example
    -------
    To run the algorithm, create a :class:`GreedyElim` instance and call `run`.

    .. code-block:: python

        >>> from cspy import GreedyElim
        >>> G = nx.DiGraph(directed=True, n_res=2)
        >>> G.add_edge('Source', 'A', res_cost=[1, 1], weight=1)
        >>> G.add_edge('Source', 'B', res_cost=[1, 1], weight=1)
        >>> G.add_edge('A', 'C', res_cost=[1, 1], weight=1)
        >>> G.add_edge('B', 'C', res_cost=[2, 1], weight=-1)
        >>> G.add_edge('C', 'D', res_cost=[1, 1], weight=-1)
        >>> G.add_edge('D', 'E', res_cost=[1, 1], weight=1)
        >>> G.add_edge('D', 'F', res_cost=[1, 1], weight=1)
        >>> G.add_edge('F', 'Sink', res_cost=[1, 1], weight=1)
        >>> G.add_edge('E', 'Sink', res_cost=[1, 1], weight=1)
        >>> max_res, min_res = [5, 5], [0, 0]
        >>> path = GreedyElim(G, max_res, min_res).run()
        >>> print(path)
        ['Source', 'A', 'C', 'D', 'E', 'Sink']

    .. _Marinakis et al. 2017: https://www.sciencedirect.com/science/article/pii/S0377221717302357
    """

    def __init__(self, G, max_res, min_res, swarm_size, member_size,
                 lower_bound, upper_bound, c1, c2, c3, max_steps,
                 min_objective=None):
        StandardGraph.__init__(self, G, max_res, min_res)
        ParticleSwarm.__init__(self, swarm_size, member_size,
                               lower_bound, upper_bound, c1, c2, c3, max_steps,
                               min_objective)

    def _objective(self, member):
        rand = random()
        path = self._get_path(self._discretise_solution(member, rand))
        return self._get_objective_from_path(path)

    def _get_path(self, arr):
        # arr contains binary representation of nodes for a path
        nodes = list(self.G.nodes())
        return [nodes[i] for i in range(len(nodes)) if arr[i] == 1]

    def _get_path_edges(self, path):
        shortest_path_edges = [
            edge for edge in self.G.edges(
                self.G.nbunch_iter(path), data=True)
            if edge[0:2] in zip(path, path[1:])]
        return shortest_path_edges

    def _save_shortest_path(self, shortest_path_edges):
        self.shortest_path = []
        self.shortest_path = list(edge[0] for edge in shortest_path_edges)
        self.shortest_path.append(shortest_path_edges[-1][1])
        if self.shortest_path:
            return any(edge[1] not in self.shortest_path
                       for edge in shortest_path_edges)

    def _get_shortest_path(self):
        return self.shortest_path

    def _get_objective_from_path(self, path):
        if len(path) == len(self.G.nodes()):
            return 1000
        shortest_path_edges = self._get_path_edges(path)
        obj = 0
        if shortest_path_edges:
            disconnected = self._save_shortest_path(shortest_path_edges)
            if disconnected:
                return 10000
            if len(shortest_path_edges) <= 5:
                obj = 10 * (6 - len(shortest_path_edges))
            if shortest_path_edges[0][0] != "Source" or shortest_path_edges[-1][1] != "Sink":
                obj += 1000
                return obj
            total_res = zeros(self.G.graph['n_res'])
            # Check path for resource feasibility by checking each edge
            for edge in shortest_path_edges:
                total_res += self._edge_extract(edge)
                if (all(total_res <= self.max_res) and
                        all(total_res >= self.min_res)):
                    pass
                else:
                    return 10000 + obj
            return sum(edge[2]['weight'] for edge in shortest_path_edges) + obj
        else:
            return 1000

    @staticmethod
    def _discretise_solution(member, rand):

        def __discrete_position(elem):
            sig = 1 / (1 + exp(-elem))
            return 1 if sig < rand else 0

        fv = vectorize(__discrete_position)
        return fv(member)

    @staticmethod
    def _edge_extract(edge):
        return array(edge[2]['res_cost'])
