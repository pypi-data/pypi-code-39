"""Exception classes for the graph package."""


class GraphException(Exception):
    """The base class for graph package exceptions."""


class EdgeNotFound(GraphException):
    """The graph does not contain the edge."""


class NodeInvalid(GraphException):
    """The node must be hashable."""


class NodeNotFound(GraphException):
    """The graph does not contain the node."""
