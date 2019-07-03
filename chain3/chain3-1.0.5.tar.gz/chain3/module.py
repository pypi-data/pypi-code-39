class Module:
    chain3 = None

    def __init__(self, chain3):
        self.chain3 = chain3

    @classmethod
    def attach(cls, target, module_name=None):
        if not module_name:
            module_name = cls.__name__.lower()

        if hasattr(target, module_name):
            raise AttributeError(
                "Cannot set {0} module named '{1}'.  The chain3 object "
                "already has an attribute with that name".format(
                    target,
                    module_name,
                )
            )

        if isinstance(target, Module):
            chain3 = target.chain3
        else:
            chain3 = target

        setattr(target, module_name, cls(chain3))
