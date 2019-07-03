from .base import SimpleCollection
from .abvariant import Abvariant, ControlAbvariant, RandomControlAbvariant, NullControlAbvariant, CustomAbvariant


class Abvariants(SimpleCollection):
    _RESOURCE = Abvariant
    _DEFAULT_SORTING = ["label", "ASC"]
    _DEFAULT_RANGE = [0, 100]

    def create(self, abvariants):
        """Adds an object to collection

        ```
        from pyprimed.models.abvariant import ControlAbvariant
        
        e.abvariants.create({ab1: 0.8, ab2: 0.1, ControlAbvariant('A': 0.1})
        ```

        :param **abvariants: abvariants and respective fractions
        :type **abvariants: dict
        :raises: AlreadyExistsException if resource by that primary key already exists
        :return: None
        """

        assert isinstance(
            abvariants, dict
        ), "abvariants should be a dictionary with as keys Abvariant objects, and fractions as values: `{ab1: 0.1, ab2: 0.9}`"

        attrs = []

        for abvariant, fraction in abvariants.items():
            if isinstance(abvariant, ControlAbvariant) or isinstance(abvariant, RandomControlAbvariant) or isinstance(abvariant, NullControlAbvariant):
                d = {"label": abvariant.label, "type": abvariant.type, "fraction": fraction }
            elif isinstance(abvariant, CustomAbvariant):
                d = abvariant.toDict(exclude=["models"])
                d["fraction"] = fraction
                d["models"] = []
                for m, weight in abvariant.models.items():
                    d["models"].append({"uid": m.uid, "weight": weight})
            else:
                raise Exception(f"Unsupported Abvariant type, was: {type(abvariant)}")

            attrs.append(d)

        self.root._dispatch_request(
            caller=self,
            operation="CREATE",
            path=self.path,
            data=list(attrs),
            params={"experiment.uid": self._parent.uid},
        )
    
    def update(self, abvariants):
        """
        Updates an abvariants in a collection

        ```python
        experiment.abvariants.update({m1: 0.5, m2: 0.5})
        ```
        """

        assert isinstance(
            abvariants, dict
        ), "abvariants should be a dictionary with as keys Abvariant objects, and fractions as values: `{ab1: 0.1, ab2: 0.9}`"

        attrs = []

        for abvariant, fraction in abvariants.items():
            if isinstance(abvariant, ControlAbvariant) or isinstance(abvariant, RandomControlAbvariant) or isinstance(abvariant, NullControlAbvariant):
                d = {"label": abvariant.label, "type": abvariant.type, "fraction": fraction }
            elif isinstance(abvariant, CustomAbvariant):
                d = abvariant.toDict(exclude=["models"])
                d["fraction"] = fraction
                d["models"] = []
                for m, weight in abvariant.models.items():
                    d["models"].append({"uid": m.uid, "weight": weight})
            else:
                raise Exception(f"Unsupported Abvariant type, was: {type(abvariant)}")

            attrs.append(d)

        self.root._dispatch_request(
            caller=self,
            operation="UPDATE",
            path=self.path,
            data=list(attrs),
            params={"experiment.uid": self._parent.uid},
        )
