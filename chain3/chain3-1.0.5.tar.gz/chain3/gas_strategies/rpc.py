def rpc_gas_price_strategy(chain3, transaction_params=None):
    """
    A simple gas price strategy deriving it's value from the mc_gasPrice JSON-RPC call.
    """
    return chain3.manager.request_blocking("mc_gasPrice", [])
