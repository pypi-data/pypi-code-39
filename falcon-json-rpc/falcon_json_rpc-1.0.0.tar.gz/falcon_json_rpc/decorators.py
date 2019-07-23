from .config import InjectedAttributes


class JsonAPIExchange:
    def __init__(self, rpc: bool = True):
        self.rpc = rpc

    def __call__(self, cls):
        class WrappedJsonExchange(cls):
            pass

        setattr(WrappedJsonExchange, InjectedAttributes.json_exchange_flag, True)
        setattr(WrappedJsonExchange, InjectedAttributes.enable_json_rpc, self.rpc)
        return WrappedJsonExchange


JsonRpc = JsonAPIExchange(rpc=True)
JsonExchange = JsonAPIExchange(rpc=False)
