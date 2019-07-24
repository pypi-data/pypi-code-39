"""An implementation of a graph structure."""

from collections.abc import Iterable

from .exceptions import EdgeNotFound
from .exceptions import NodeInvalid
from .exceptions import NodeNotFound


class Graph(dict):
    """A datastructure representing a graph.

    The datastructure exposes methods to manipulate nodes
    and edges trough their respective namespaces.
    """

    def __init__(self):
        """See class documentation."""
        super().__init__()
        self.nodes = Nodes(self)
        self.edges = Edges(self)


class Nodes:
    """A namespace containing methods to manipulate nodes in a graph.

    Args:
        graph: The graph to manipulate.
    """

    def __init__(self, graph):
        """See class documentation."""
        self.graph = graph

    def add(self, *nodes):
        """Add nodes to the graph.
        
        Args:
            nodes: Hashable objects to add to the graph.
        
        Raises:
            NodeInvalid
        """
        check_hashable(*nodes)

        for node in nodes:
            self.graph.setdefault(node, dict())

    def preceding(self, node):
        """Find all nodes preceding this node in the graph.

        Args:
            node: A hashable object.
        
        Yields:
            All nodes with an edge to this node.
        
        Raises:
            NodeInvalid, NodeNotFound
        """
        check_hashable(node)

        if node in self.graph:
            for preceding, succeeding in self.graph.items():
                if node in succeeding:
                    yield preceding
        else:
            raise NodeNotFound

    def succeeding(self, node):
        """Find all nodes succeeding this node in the graph.

        Args:
            node: A hashable object.
        
        Yields:
            All nodes with an edge from this node.
        
        Raises:
            NodeInvalid, NodeNotFound
        """
        check_hashable(node)

        try:
            for succeeding in self.graph[node]:
                yield succeeding
        except KeyError as exception:
            raise NodeNotFound from exception

    def discard(self, node):
        """Remove a node and all its edges, if it exists.
        
        Args:
            node: A hashable object.
        
        Raises:
            NodeInvalid
        """
        try:
            self.remove(node)
        except NodeNotFound:
            pass

    def remove(self, node):
        """Remove a node and all its edges, if it exists, else fail.
        
        Args:
            node: A hashable object.
        
        Raises:
            NodeInvalid, NodeNotFound
        """
        for preceding in list(self.preceding(node)):
            del self.graph[preceding][node]
        del self.graph[node]

    def __iter__(self):
        yield from self.graph


class Edge(Iterable):
    """A proxy class representing an edge in the graph.
    
    Args:
        graph: The graph referenced.
        preceding: The node preceding this edge.
        succeeding: The node succeeding this edge.
    """

    def __init__(self, graph, preceding, succeeding):
        """See class documentation."""
        self.graph = graph

        self._preceding = preceding
        self._succeeding = succeeding

    @property
    def preceding(self):
        """The node preceding this edge."""
        return self._preceding

    @property
    def succeeding(self):
        """The node succeeding this edge."""
        return self._succeeding

    @property
    def value(self):
        """The value of this edge."""
        return self.graph.edges.value(self.preceding, self.succeeding)

    @value.setter
    def value(self, value):
        self.graph.edges.update(self.preceding, self.succeeding, value)

    def __iter__(self):
        yield self.preceding
        yield self.succeeding


class Edges:
    """A namespace containing methods to manipulate edges in a graph.

    Args:
        graph: The graph to manipulate.
    """

    def __init__(self, graph):
        """See class documentation."""
        self.graph = graph

    def update(self, preceding, succeeding, value=None):
        """Add or update an edge in the graph.

        This will add the nodes if they do not exist yet.
        
        Args:
            preceding: A hashable object.
            succeeding: A hashable object.
            value: A value to associate with this edge, defaults to None.

        Raises:
            NodeInvalid
        """
        check_hashable(preceding, succeeding)

        self.graph.setdefault(succeeding, dict())
        self.graph.setdefault(preceding, dict())[succeeding] = value

    def value(self, preceding, succeeding):
        """Find the value associated with an edge.

        Args:
            preceding: A hashable object.
            succeeding: A hashable object."
        
        Returns:
            The value associated with this edge.

        Raises:
            EdgeNotFound, NodeInvalid
        """
        check_hashable(preceding, succeeding)

        try:
            return self.graph[preceding][succeeding]
        except KeyError as exception:
            raise EdgeNotFound from exception

    def preceding(self, node):
        """Find all edges preceding this node in the graph.

        Args:
            node: A hashable object.
        
        Yields:
            All edges to this node.
        
        Raises:
            NodeNotFound, NodeInvalid
        """
        check_hashable(node)

        if node in self.graph:
            for preceding, succeeding in self.graph.items():
                if node in succeeding:
                    yield Edge(self.graph, preceding, node)
        else:
            raise NodeNotFound

    def succeeding(self, node):
        """Find all edges succeeding this node in the graph.

        Args:
            node: A hashable object.
        
        Yields:
            All edges from this node.
        
        Raises:
            NodeNotFound, NodeInvalid
        """
        check_hashable(node)

        try:
            for succeeding in self.graph[node]:
                yield Edge(self.graph, node, succeeding)
        except KeyError as exception:
            raise NodeNotFound from exception

    def discard(self, preceding, succeeding):
        """Remove an edge, if it exists.
        
        Args:
            preceding: A hashable object.
            succeeding: A hashable object.
        
        Raises:
            NodeInvalid
        """
        try:
            self.remove(preceding, succeeding)
        except EdgeNotFound:
            pass

    def remove(self, preceding, succeeding):
        """Remove an edge, if it exists, else fail.
        
        Args:
            preceding: A hashable object.
            succeeding: A hashable object.
        
        Raises:
            EdgeNotFound, NodeInvalid
        """
        check_hashable(preceding, succeeding)

        try:
            del self.graph[preceding][succeeding]
        except KeyError as exception:
            raise EdgeNotFound from exception

    def __iter__(self):
        for preceding in self.graph:
            for succeeding in self.graph[preceding]:
                yield Edge(self.graph, preceding, succeeding)


def check_hashable(*nodes):
    """Check if all nodes are hashable.
    
    Args:
        nodes: Objects to be checked.
    
    Raises:
        NodeInvalid
    """
    for node in nodes:
        try:
            hash(node)
        except TypeError as exception:
            raise NodeInvalid from exception
