import traceback
from collections import OrderedDict
from itertools import chain
from typing import Iterator, List, Any, Callable, Optional, Tuple, Set, Iterable
from uuid import uuid4, UUID

import networkx as nx


def generate_flows(graph: nx.DiGraph) -> Iterator[List[Tuple[Any, Set[Any]]]]:
    assert nx.is_directed_acyclic_graph(graph)
    assert all(not attr.get('simple', False) or graph.out_degree(n) == 0 for n, attr in graph.nodes(data=True))
    roots = [n for n in graph.nodes if graph.in_degree(n) == 0]
    for root in roots:
        path: List[Tuple[Any, Set[Any]]] = []
        is_new_path = True
        for u, v, d in nx.dfs_labeled_edges(graph, root):
            is_simple = graph.node[v].get('simple', False)
            if d == 'forward':
                if is_simple:
                    path[-1][1].add(v)
                else:
                    path.append((v, set()))
                    is_new_path = True
            elif d == 'reverse':
                if is_new_path:
                    yield list(path)
                    is_new_path = False
                if not is_simple:
                    del path[-1]
            elif d == 'nontree':
                # ignored but should not happen in a DAG
                pass
            else:
                yield ValueError('Unexpected direction: {}'.format(d))


class Flow(object):
    def __init__(self, graph: nx.DiGraph, path: List[Tuple[Any, Set[Any]]]):
        super(Flow, self).__init__()
        self.graph = graph
        self.path = path
        self.last_node = None
        self.executed_path: List[Tuple[Any, Set[Any]]] = []
        self.cleanups: List[Callable] = list()

    def _run_step(self, step: Tuple[Any, Set[Any]], *inputs: Any) -> Any:
        node, test_steps = step
        step_function = self.graph.node[node]['step_function']
        cleanup_callback = self.graph.node[node]['cleanup']
        print('  run {}'.format(step_function.__name__))
        self.last_node = node
        self.executed_path.append((node, set()))
        data = step_function(*inputs)
        if cleanup_callback is not None:
            self.cleanups.append(lambda: cleanup_callback(data))
        for test_step in test_steps:
            step_function = self.graph.node[test_step]['step_function']
            print('    run test {}'.format(step_function.__name__))
            self.last_node = test_step
            self.executed_path[-1][1].add(test_step)
            step_function(data)
        return data

    def run(self):
        try:
            data = self._run_step(self.path[0])
            for step in self.path[1:]:
                data = self._run_step(step, data)
            self.last_node = None
        finally:
            if self.cleanups:
                print('Running {} cleanup actions'.format(len(self.cleanups)))
            for cleanup_action in self.cleanups:
                cleanup_action()

    @property
    def step_names(self) -> List[str]:
        return [self.graph.node[node]['step_function'].__name__ for node, tests in self.path]

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


class NodeSet(object):
    def __init__(self, idlist: Optional[Iterable[UUID]] = None):
        super(NodeSet, self).__init__()
        self._idlist = set(idlist) if idlist is not None else set()

    def add(self, id: UUID):
        self._idlist.add(id)


class FlowGraph(object):
    def __init__(self):
        super(FlowGraph, self).__init__()
        self.graph = nx.DiGraph()

    def add_start(self, step_function: Callable, cleanup: Optional[Callable]) -> NodeSet:
        id = uuid4()
        self.graph.add_node(id, step_function=step_function, start=True, simple=False, cleanup=cleanup)
        return NodeSet([id])

    def add_followup(self, step_function: Callable, parents: List[NodeSet], simple: bool, cleanup: Optional[Callable]) -> NodeSet:
        assert cleanup is None or not simple, 'Simple nodes cannot have a cleanup callback'
        parent_id_set = set(chain.from_iterable(ns._idlist for ns in parents))
        result = NodeSet()
        for parent in parent_id_set:
            id = uuid4()
            self.graph.add_node(id, step_function=step_function, start=False, simple=simple, cleanup=cleanup)
            self.graph.add_edge(parent, id)
            result.add(id)
        return result

    def flows(self) -> Iterator[Flow]:
        for path in generate_flows(self.graph):
            yield Flow(self.graph, path)

    def step_decorator(self, *parents: NodeSet, simple: bool = False, cleanup: Optional[Callable] = None) -> Callable[[Callable], NodeSet]:
        def decorator(step_function: Callable) -> NodeSet:
            if not parents:
                assert not simple, 'Start nodes cannot be simple'
                return self.add_start(step_function, cleanup=cleanup)
            else:
                return self.add_followup(step_function, list(parents), simple, cleanup)
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
