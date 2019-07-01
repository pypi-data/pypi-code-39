import traceback
from collections import OrderedDict
from typing import Iterator, List, Any, Callable, Optional
from uuid import uuid4, UUID

import networkx as nx


def generate_flows(graph: nx.DiGraph) -> Iterator[List[Any]]:
    assert nx.is_directed_acyclic_graph(graph)
    roots = [n for n in graph.nodes if graph.in_degree(n) == 0]
    for root in roots:
        path = []
        is_new_path = True
        for u, v, d in nx.dfs_labeled_edges(graph, root):
            if d == 'forward':
                path.append(v)
                is_new_path = True
            elif d == 'reverse':
                if is_new_path:
                    yield list(path)
                    is_new_path = False
                del path[-1]
            elif d == 'nontree':
                # ignored but should not happen in a DAG
                pass
            else:
                yield ValueError('Unexpected direction: {}'.format(d))


class Flow(object):
    def __init__(self, graph: nx.DiGraph, path: List[Any]):
        super(Flow, self).__init__()
        self.graph = graph
        self.path = path
        self.last_node = None
        self.executed_path = []

    def run(self):
        start = self.path[0]
        step_function = self.graph.node[start]['step_function']
        self.last_node = start
        self.executed_path.append(start)
        data = step_function()
        for node in self.path[1:]:
            step_function = self.graph.node[node]['step_function']
            self.last_node = node
            self.executed_path.append(node)
            data = step_function(data)
        self.last_node = None

    @property
    def step_names(self) -> List[str]:
        return [self.graph.node[node]['step_function'].__name__ for node in self.path]

    @property
    def path_str(self) -> str:
        return ' -> '.join(self.step_names)

    @property
    def last_step_name(self) -> str:
        if self.last_node is not None:
            return self.graph.node[self.last_node]['step_function'].__name__
        else:
            return ''

    def starts_with(self, path: List[Any]) -> bool:
        return self.path[:len(path)] == path


class FlowGraph(object):
    def __init__(self):
        super(FlowGraph, self).__init__()
        self.graph = nx.DiGraph()

    def add_start_node(self, step_function: Callable) -> UUID:
        id = uuid4()
        self.graph.add_node(id, step_function=step_function, start=True)
        return id

    def add_followup_node(self, step_function: Callable, parent: UUID) -> UUID:
        id = uuid4()
        self.graph.add_node(id, step_function=step_function, start=False)
        self.graph.add_edge(parent, id)
        return id

    def flows(self) -> Iterator[Flow]:
        for path in generate_flows(self.graph):
            yield Flow(self.graph, path)

    def step_decorator(self, parent: Optional[Callable] = None):
        def decorator(step_function: Callable) -> Callable:
            if parent is None:
                step_function.step_id = self.add_start_node(step_function)
            else:
                step_function.step_id = self.add_followup_node(step_function, parent.step_id)
            return step_function
        return decorator

    def run_all_flows(self):
        results = OrderedDict()
        ignore_paths = list()
        all_ok = True
        for index, flow in enumerate(self.flows()):
            print('Flow {}:'.format(flow.path_str))
            if any(flow.starts_with(path) for path in ignore_paths):
                print('IGNORE')
                results[flow.path_str] = 'IGNORE'
                continue
            try:
                flow.run()
            except:
                traceback.print_exc()
                print('ERROR in {}'.format(flow.last_step_name))
                results[flow.path_str] = ' ERROR'
                ignore_paths.append(flow.executed_path)
                all_ok = False
            else:
                print('OK')
                results[flow.path_str] = '    OK'

        print()
        if all_ok:
            print('All flows have passed')
        else:
            print('Not all flows have passed. Summary:')
            print('\n'.join('{} {}'.format(result, path) for path, result in results.items()))
        return all_ok
