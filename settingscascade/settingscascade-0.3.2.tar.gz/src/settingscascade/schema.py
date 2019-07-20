import typing
from inspect import getmro


class ElementSchemaMeta(type):
    def __new__(cls, name, parents, dct):
        __props__ = {}
        for parent in parents:
            classes = reversed(getmro(parent))
            for klass in classes:
                __props__.update(getattr(klass, "__annotations__", {}))
        __props__.update(dct.get("__annotations__", {}))
        __props__.pop("_name_")
        dct["_name_"] = dct.get("_name_", name.lower())
        dct["__props__"] = __props__
        return super().__new__(cls, name, parents, dct)


class ElementSchema(metaclass=ElementSchemaMeta):
    """Class that defines the schema for a particular element in your
    settings heirarchy. Subclass this and add annotations to define
    the allowed values for this element type-

    .. code-block:: python

        class Element(ElementSchema):
            color: str
            height: int

    """

    _name_: str = "config"
    _manager_ = None
    _klass_ = None
    _id_ = None

    def __init__(self, configManager):
        self._manager_ = configManager

    def __call__(self, name=None, identifier=None):
        self._klass_ = name
        self._id_ = identifier
        return self

    @property
    def context(self):
        """The context stack that will be used to look up settings for this object"""
        base = self._name_
        if self._klass_:
            base += f".{self._klass_}"
        if self._id_:
            base += f"#{self._id_}"
        return base

    def __getattr__(self, item):
        if item not in self.__props__:
            raise AttributeError()
        with self._manager_.context(self.context):
            return getattr(self._manager_, item)

    def load(self):
        """Loads the settings for this schema into a python dictionary. Looks up the value for
        each property using the current context stack for this object.

        .. note::

            This will throw an error if there are settings defined on the schema that can't be
            found in any level!
        """
        return {key: getattr(self, key) for key in self.__props__}

    @classmethod
    def check_type(cls, key, val):
        if key not in cls.__props__:
            raise ValueError(f"{key} is not valid for {cls._name_}")

        type_hint = cls.__props__[key]
        if isinstance(
            type_hint, typing._SpecialForm  # pylint: disable=protected-access
        ):
            # No check for typing.Any, typing.Union, typing.ClassVar (without parameters)
            return
        try:
            actual_type = type_hint.__origin__
        except AttributeError:
            actual_type = type_hint
        if isinstance(
            actual_type, typing._SpecialForm  # pylint: disable=protected-access
        ):
            # case of typing.Union[…] or typing.ClassVar[…]
            actual_type = type_hint.__args__

        if not isinstance(val, actual_type):
            raise TypeError(
                f"Unexpected type for {key} in element {cls._name_} "
                f"expected {actual_type} but found {type(val)}"
            )
