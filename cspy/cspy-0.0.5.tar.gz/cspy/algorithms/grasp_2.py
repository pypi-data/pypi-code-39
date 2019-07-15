from __future__ import absolute_import
from __future__ import print_function

import logging
import numpy as np
from random import sample
# from networkx import astar_path, NetworkXException
from cspy.preprocessing import check
from cspy.path import Path

log = logging.getLogger(__name__)


class GRASP:
    """
    Greedy Randomised Adaptive Search Procedure for the (resource) constrained
    shortest path problem.

    Parameters
    ----------
    G : object instance :class:`nx.Digraph()`
        must have ``n_res`` graph attribute and all edges must have
        ``res_cost`` attribute. Also, the number of nodes must be
        :math:`\geq 5`.

    max_res : list of floats
        :math:`[M_1, M_2, ..., M_{n\_res}]` upper bounds for resource
        usage (including initial forward stopping point).

    min_res : list of floats
        :math:`[L_1, L_2, ..., L_{n\_res}]` lower bounds for resource
        usage (including initial backward stopping point).
        We must have ``len(min_res)`` :math:`=` ``len(max_res)``.

    max_iter : int
        Maximum number of iterations for algorithm

    max_no_improvement : int
        Maximum number of iterations without improvement

    alpha : float, optional
        Greediness factor 0 (random) --> 1 (greedy)

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
    The input graph must have a ``n_res`` attribute.
    The edges in the graph must all have a ``res_cost`` attribute.
    See `Using cspy`_

    .. _Using cspy: https://cspy.readthedocs.io/en/latest/how_to.html


    Example
    -------
    To run the algorithm, create a :class:`GRASP` instance and call `run`.

    .. code-block:: python

        >>> from cspy import GRASP
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
        >>> path = GRASP(G, max_res, min_res).run()
        >>> print(path)
        ['Source', 'A', 'C', 'D', 'E', 'Sink']

    """

    def __init__(self, G, max_res, min_res, max_iter, max_no_improvement,
                 alpha=0.9):
        # Check input graph and parameters
        # check(G, max_res, min_res)
        # Input parameters
        self.G = G
        self.max_res = max_res
        self.min_res = min_res
        self.max_iter = max_iter
        self.max_no_improvement = max_no_improvement
        self.alpha = alpha
        # Algorithm specific parameters
        self.it = 0
        self.best = None
        self.stop = False
        self.nodes = self.G.nodes()
        # list(node for node in self.G.nodes()
        #                   if node != 'Source' and node != 'Sink')

    def run(self):
        while self.it < self.max_iter and not self.stop:
            self.algorithm()
            self.it += 1
        return self.best['list']

    def algorithm(self):
        solution = self._construct()
        solution = self._local_search(solution)
        self._update_best(solution)

    def _construct(self):
        # TODO maybe make solution into an object
        solution = {'list': sample(self.nodes, 1),
                    'cost': 0}
        candidates = []
        while not self._check_path(solution):
            candidates = [i for i in self.nodes
                          if i not in solution['list']]
            weights = [self._heuristic(solution['list'][-1], i)
                       for i in candidates]
            # Build Restricted Candidiate List
            restriced_candidates = [
                candidates[i] for i, c in enumerate(weights)
                if c <= (min(weights) +
                         self.alpha * (max(weights) - min(weights)))]
            solution['list'].append(np.random.choice(restriced_candidates))
            solution['cost'] = self._cost_solution(solution)
            if len(solution['list']) >= len(self.nodes):
                solution = {'list': sample(self.nodes, 1),
                            'cost': 0}
        else:  # Resource feasible path found
            self.stop = True
        return solution

    def _local_search(self, solution):
        it = 0
        while it < self.max_no_improvement:
            candidate = {'list': self._stochastic_two_opt(solution['list'])}
            candidate['cost'] = self._cost_solution(candidate)
            if candidate['cost'] < solution['cost']:
                solution = candidate
            it += 1
        return solution

    def _update_best(self, solution):
        if not self.best or solution['cost'] < self.best['cost']:
            self.best = solution

    def _heuristic(self, i, j):
        # Given a node pair returns a weight to apply
        if i and j:
            if (i, j) not in self.G.edges():
                return 1e10
            else:
                return self.G.get_edge_data(i, j)['weight']
        else:
            return 1e10

    def _cost_solution(self, solution):
        return sum(self._heuristic(i, j)
                   for i, j in zip(solution['list'],
                                   solution['list'][1:]))

    def _check_path(self, solution):
        # TODO add resource feasibility check
        path, cost = solution['list'], solution['cost']
        if (len(path) > 2 and cost < 1e10 and
                path[0] == 'Source' and
                path[-1] == 'Sink'):
            if Path(self.G, path)._check_feasibility(
                    self.max_res, self.min_res):
                return True
            else:
                return False
        else:
            return False
        pass

    @staticmethod
    def _stochastic_two_opt(permutation):
        reduced_list = [elem for elem in permutation
                        if elem != "Source" and elem != "Sink"]
        perm_size = len(reduced_list)
        if perm_size <= 3:
            return permutation
        x = list(reduced_list)
        start, end = sorted(sample(range(perm_size), 2))
        exclude = [start]
        exclude.append(perm_size - 1 if start == 0 else start - 1)
        exclude.append(0 if start == perm_size - 1 else start + 1)
        while end in exclude:
            end = sample(range(perm_size), 1)[0]
        if end < start:
            start, end = end, start
        return (["Source"] + x[:start] +
                list(reversed(x[start:end])) +
                x[end:] + ["Sink"])
