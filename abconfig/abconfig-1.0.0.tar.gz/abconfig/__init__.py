__version__ = '1.0.0'

from abconfig.common import Dict
from abconfig.utils import Attrs, Finalize
from abconfig.file import Json, Yaml
from abconfig.env import Env


class ABConfig(Dict):
    def __init__(self):
        if str(type(self).__name__) == 'ABConfig':
            raise NotImplementedError

        super().__init__(
            Attrs(self) \
            .bind(Json) \
            .bind(Yaml) \
            .bind(Env)  \
            .bind(Finalize)
        )
