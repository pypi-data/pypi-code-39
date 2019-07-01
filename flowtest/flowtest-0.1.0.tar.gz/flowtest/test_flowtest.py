import unittest

import networkx as nx

from flowtest import generate_flows


class TestScheduling(unittest.TestCase):
    def test_generate_flows_01(self):
        graph = nx.DiGraph()
        graph.add_path([1, 2, 3, 4, 5])
        flows = list(generate_flows(graph))
        expected_flows = [
            [1, 2, 3, 4, 5],
        ]
        self.assertEqual(expected_flows, flows)

    def test_generate_flows_02(self):
        graph = nx.DiGraph()
        graph.add_path([1, 2, 3, 4, 5])
        graph.add_path([4, 6])
        flows = list(generate_flows(graph))
        expected_flows = [
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 6],
        ]
        self.assertEqual(expected_flows, flows)
