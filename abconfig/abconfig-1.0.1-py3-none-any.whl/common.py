from collections import UserDict


class Item:
    """ Converting an item type to type from a related subset of types.

    (+) - converting the type of second operand to type of the first operand.
    Values ​​are not sum, the first operand will be replaced by the second.
    When trying to convert an element type to a type that belongs another subset
    is thrown TypeError is raised. For example, you cannot convert a list, tuple and
    set to bool or string, a string cannot be converted to a list, tuple or set.
    This is different from the default behavior in Python.
    """

    mempty = None

    defined_sets = (
        [int, float, str, bool],
        [list, tuple, set]
    )

    def __init__(self, x):
        if x != self.mempty:
            self.current_type = self._detect_type(x)
            self.current_set = [
                s for s in self.defined_sets
                if self.current_type in s
            ][0]
        self.data = x

    def _detect_type(self, x):
        return x if isinstance(x, type) else type(x)

    def __add__(self, operand):
        if self.data == self.mempty:
            return operand
        elif operand == self.mempty or isinstance(operand, type):
            return self.data
        elif not self._detect_type(operand) in self.current_set:
            raise TypeError
        else:
            return self.current_type(operand)


class Dict(UserDict):
    """ Wrapper to build a dictionary processing chain.

    (+) - atomic update values ​​of the first dictionary
    to values ​​from second dictionary with support recursive processing
    nested dictionaries.

    fmap - applies function to each pair of key values
    ​​in dictionary currently stored in object.

    bind - applies function to self object.
    """

    mempty = dict()

    def fmap(self, f):
        return Dict(map(f, self.items()))

    def bind(self, k):
        return k(self)

    def __add__(self, operand: dict):
        if operand == self.mempty:
            return self.data
        elif self.data == self.mempty:
            return operand

        return self.fmap(lambda x:
            (x[0], Dict(x[1]) + operand.get(x[0], self.mempty))
            if isinstance(x[1], (dict, Dict)) else
            (x[0], Item(x[1]) + operand.get(x[0], Item.mempty))
        )
