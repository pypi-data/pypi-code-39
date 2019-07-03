from chain3.module import (
    Module,
)


class Net(Module):
    @property
    def listening(self):
        return self.chain3.manager.request_blocking("net_listening", [])

    @property
    def peerCount(self):
        return self.chain3.manager.request_blocking("net_peerCount", [])

    @property
    def chainId(self):
        return None

    @property
    def version(self):
        return self.chain3.manager.request_blocking("net_version", [])
