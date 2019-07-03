from chain3.module import (
    Module,
)


class Version(Module):
    @property
    def api(self):
        from chain3 import __version__
        return __version__

    @property
    def node(self):
        return self.chain3.manager.request_blocking("chain3_clientVersion", [])

    @property
    def network(self):
        return self.chain3.manager.request_blocking("net_version", [])

    @property
    def ethereum(self):
        return self.chain3.manager.request_blocking("mc_protocolVersion", [])
