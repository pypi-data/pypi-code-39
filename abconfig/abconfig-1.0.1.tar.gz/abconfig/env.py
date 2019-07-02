from os import environ
from abconfig.common import Dict


class Env(Dict):
    def __init__(self, x):
        enabled = x.pop('load_env', True)
        if enabled != False:
            super().__init__(x + self._read(x))
        else:
            super().__init__(x)

    def _read(self, x, prefix=None):
        return dict(map(lambda i:
            (i[0], self._read(i[1], self._get_prefix(prefix,i[0])))
            if isinstance(i[1], (dict, Dict)) else
            (i[0], environ.get(self._get_prefix(prefix, i[0]).upper(), None)),
            x.items())
        )

    def _get_prefix(self, *args):
        return '_'.join(filter(lambda x: True if x else False, args))
