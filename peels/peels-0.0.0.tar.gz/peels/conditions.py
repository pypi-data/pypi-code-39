from typing import Any, Dict


class Condition:

    def __init__(self, target: str):
        self.target = target

    def __call__(self, ctx: Dict[str, Any], label: str):
        raise NotImplemented


class ValueCondition(Condition):

    def __call__(self, ctx: Dict[str, Any], _):
        return ctx[self.target]


class EnabledCondition(Condition):

    def __call__(self, ctx: Dict[str, Any], _):
        return self.target in ctx
