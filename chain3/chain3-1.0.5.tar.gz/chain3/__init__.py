import pkg_resources
import sys

if sys.version_info < (3, 5):
    raise EnvironmentError("Python 3.5 or above is required")

from mc_account import Account  # noqa: E402
from chain3.main import Chain3  # noqa: E402
from chain3.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from chain3.providers.mc_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from chain3.providers.tester import (  # noqa: E402
    TestRPCProvider,
)
from chain3.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from chain3.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

#__version__ = pkg_resources.get_distribution("chain3").version

__version__ = '0.0.1'

__all__ = [
    "__version__",
    "Chain3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "EthereumTesterProvider",
    "Account",
]
