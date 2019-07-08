from .node import _Node
from .link import _Link
from .metadata import Metadata


def _get_all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        (s for c in cls.__subclasses__() for s in _get_all_subclasses(c))
    )


class _ElementAccess:
    _elements = {}

    @classmethod
    def __getitem__(cls, key):
        return cls._elements[key]

    @classmethod
    def items(cls):
        return cls._elements.items()

    @classmethod
    def instantiate(cls, attribute_mapping, validate_normalize=True):
        class_name = attribute_mapping.get("type", None)
        if not class_name:
            raise ValueError("Cannot instantiate: missing attribute 'type'")
        element_class = cls._elements.get(class_name, None)
        if not element_class:
            raise ValueError(
                "Model type {} not found in {}".format(class_name, cls.__name__)
            )
        return element_class(**attribute_mapping, validate_normalize=validate_normalize)


class Nodes(_ElementAccess):
    _elements = {
        element_class.__name__: element_class
        for element_class in _get_all_subclasses(_Node)
        if not element_class.__name__.startswith("_")
    }


class Links(_ElementAccess):
    _elements = {
        element_class.__name__: element_class
        for element_class in _get_all_subclasses(_Link)
        if not element_class.__name__.startswith("_")
    }
