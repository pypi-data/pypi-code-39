from mc_utils import (
    to_dict,
)

from chain3.utils.abi import (
    map_abi_data,
)
from chain3.utils.formatters import (
    apply_formatter_at_index,
)
from chain3.utils.toolz import (
    curry,
)

TRANSACTION_PARAMS_ABIS = {
    'data': 'bytes',
    'from': 'address',
    'gas': 'uint',
    'gasPrice': 'uint',
    'nonce': 'uint',
    'to': 'address',
    'value': 'uint',
}

# add for subchain
TRANSACTION_PARAMS_SUBCHAIN_ABIS = {
    'data': 'bytes',
    'from': 'address',
    'gas': 'uint',
    'gasPrice': 'uint',
    'nonce': 'uint',
    'to': 'address',
    'value': 'uint',
    'gasPrice': 'uint',
    'shardingFlag': 'uint',
    #'via': 'address',
}

FILTER_PARAMS_ABIS = {
    'to': 'address',
}

RPC_ABIS = {
    # mc
    'mc_call': TRANSACTION_PARAMS_ABIS,
    'mc_estimateGas': TRANSACTION_PARAMS_ABIS,
    'mc_getBalance': ['address', None],
    'mc_getBlockByHash': ['bytes32', 'bool'],
    'mc_getBlockTransactionCountByHash': ['bytes32'],
    'mc_getCode': ['address', None],
    'mc_getLogs': FILTER_PARAMS_ABIS,
    'mc_getStorageAt': ['address', 'uint', None],
    'mc_getTransactionByBlockHashAndIndex': ['bytes32', 'uint'],
    'mc_getTransactionByHash': ['bytes32'],
    'mc_getTransactionCount': ['address', None],
    'mc_getTransactionReceipt': ['bytes32'],
    'mc_getUncleCountByBlockHash': ['bytes32'],
    'mc_newFilter': FILTER_PARAMS_ABIS,
    'mc_sendRawTransaction': ['bytes'],
    'mc_sendTransaction': TRANSACTION_PARAMS_SUBCHAIN_ABIS,
    'mc_sign': ['address', 'bytes'],
    # personal
    'personal_sendTransaction': TRANSACTION_PARAMS_SUBCHAIN_ABIS,
}


@curry
def apply_abi_formatters_to_dict(normalizers, abi_dict, data):
    fields = list(set(abi_dict.keys()) & set(data.keys()))
    formatted_values = map_abi_data(
        normalizers,
        [abi_dict[field] for field in fields],
        [data[field] for field in fields],
    )
    formatted_dict = dict(zip(fields, formatted_values))
    return dict(data, **formatted_dict)


@to_dict
def abi_request_formatters(normalizers, abis):
    for method, abi_types in abis.items():
        if isinstance(abi_types, list):
            yield method, map_abi_data(normalizers, abi_types)
        elif isinstance(abi_types, dict):
            single_dict_formatter = apply_abi_formatters_to_dict(normalizers, abi_types)
            yield method, apply_formatter_at_index(single_dict_formatter, 0)
        else:
            raise TypeError("ABI definitions must be a list or dictionary, got %r" % abi_types)
