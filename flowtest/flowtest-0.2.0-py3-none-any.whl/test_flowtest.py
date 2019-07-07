import unittest

import networkx as nx

from flowtest import generate_flows


class TestScheduling(unittest.TestCase):
    def test_generate_flows_01(self):
        graph = nx.DiGraph()
        nx.add_path(graph, [1, 2, 3, 4, 5])
        flows = list(generate_flows(graph))
        expected_flows = [
            [(x, set()) for x in [1, 2, 3, 4, 5]],
        ]
        self.assertEqual(expected_flows, flows)

    def test_generate_flows_02(self):
        graph = nx.DiGraph()
        nx.add_path(graph, [1, 2, 3, 4, 5])
        nx.add_path(graph, [4, 6])
        flows = list(generate_flows(graph))
        expected_flows = [
            [(x, set()) for x in [1, 2, 3, 4, 5]],
            [(x, set()) for x in [1, 2, 3, 4, 6]],
        ]
        self.assertEqual(expected_flows, flows)

    def test_generate_flows_03(self):
        graph = nx.DiGraph()
        nx.add_path(graph, [1, 2, 3])
        graph.add_nodes_from(list('abc'), simple=True)
        graph.add_edge(1, 'a')
        graph.add_edge(2, 'b')
        graph.add_edge(2, 'c')
        flows = list(generate_flows(graph))
        expected_flows = [
            [(1, {'a'}), (2, {'b', 'c'}), (3, set())]
        ]
        self.assertEqual(expected_flows, flows)
