import math

from chain3.utils.threads import (
    Timeout,
)
from chain3.utils.toolz import (
    assoc,
    curry,
    merge,
)
from cytoolz import (
    dissoc,
)

VALID_TRANSACTION_PARAMS = [
    'from',
    'to',
    'gas',
    'gasPrice',
    'value',
    'data',
    'nonce',
    'chainId',
    #'shardingFlag',   # add for subchain
    #'via',   # add for subchain
]

TRANSACTION_DEFAULTS = {
    'value': 0,
    'data': b'',
    'gas': lambda chain3, tx: chain3.mc.estimateGas(tx),
    'gasPrice': lambda chain3, tx: chain3.mc.generateGasPrice(tx) or chain3.mc.gasPrice,
    'chainId': lambda chain3, tx: chain3.net.chainId,
    'shardingFlag': 0,
    'via': '0x0000000000000000000000000000000000000000',
}


@curry
def fill_nonce(chain3, transaction):
    if 'from' in transaction and 'nonce' not in transaction:
        return assoc(
            transaction,
            'nonce',
            chain3.mc.getTransactionCount(
                transaction['from'],
                block_identifier='pending'))
    else:
        return transaction


@curry
def fill_transaction_defaults(chain3, transaction):
    '''
    if chain3 is None, fill as much as possible while offline
    '''
    defaults = {}
    for key, default_getter in TRANSACTION_DEFAULTS.items():
        if key not in transaction:
            if callable(default_getter):
                if chain3 is not None:
                    default_val = default_getter(chain3, transaction)
                else:
                    raise ValueError("You must specify %s in the transaction" % key)
            else:
                default_val = default_getter
            defaults[key] = default_val
    return merge(defaults, transaction)


def wait_for_transaction_receipt(chain3, txn_hash, timeout=120, poll_latency=0.1):
    with Timeout(timeout) as _timeout:
        while True:
            txn_receipt = chain3.mc.getTransactionReceipt(txn_hash)
            if txn_receipt is not None:
                break
            _timeout.sleep(poll_latency)
    return txn_receipt


def get_block_gas_limit(chain3, block_identifier=None):
    if block_identifier is None:
        block_identifier = chain3.mc.blockNumber
    block = chain3.mc.getBlock(block_identifier)
    return block['gasLimit']


def get_buffered_gas_estimate(chain3, transaction, gas_buffer=100000):
    gas_estimate_transaction = dict(**transaction)

    # add for sub chain
    if 'shardingFlag' in gas_estimate_transaction:
        gas_estimate_transaction = dissoc(gas_estimate_transaction, 'shardingFlag')
    if 'via' in gas_estimate_transaction:
        gas_estimate_transaction = dissoc(gas_estimate_transaction, 'via')

    gas_estimate = chain3.mc.estimateGas(gas_estimate_transaction)

    gas_limit = get_block_gas_limit(chain3)

    if gas_estimate > gas_limit:
        raise ValueError(
            "Contract does not appear to be deployable within the "
            "current network gas limits.  Estimated: {0}. Current gas "
            "limit: {1}".format(gas_estimate, gas_limit)
        )

    return min(gas_limit, gas_estimate + gas_buffer)


def get_required_transaction(chain3, transaction_hash):
    current_transaction = chain3.mc.getTransaction(transaction_hash)
    if not current_transaction:
        raise ValueError('Supplied transaction with hash {} does not exist'
                         .format(transaction_hash))
    return current_transaction


def extract_valid_transaction_params(transaction_params):
    extracted_params = {key: transaction_params[key]
                        for key in VALID_TRANSACTION_PARAMS if key in transaction_params}

    if extracted_params.get('data') is not None:
        if transaction_params.get('input') is not None:
            if extracted_params['data'] != transaction_params['input']:
                msg = 'failure to handle this transaction due to both "input: {}" and'
                msg += ' "data: {}" are populated. You need to resolve this conflict.'
                err_vals = (transaction_params['input'], extracted_params['data'])
                raise AttributeError(msg.format(*err_vals))
            else:
                return extracted_params
        else:
            return extracted_params
    elif extracted_params.get('data') is None:
        if transaction_params.get('input') is not None:
            return assoc(extracted_params, 'data', transaction_params['input'])
        else:
            return extracted_params
    else:
        raise Exception("Unreachable path: transaction's 'data' is either set or not set")


def assert_valid_transaction_params(transaction_params):
    for param in transaction_params:
        if param not in VALID_TRANSACTION_PARAMS:
            raise ValueError('{} is not a valid transaction parameter'.format(param))


def prepare_replacement_transaction(chain3, current_transaction, new_transaction):
    if current_transaction['blockHash'] is not None:
        raise ValueError('Supplied transaction with hash {} has already been mined'
                         .format(current_transaction['hash']))
    if 'nonce' in new_transaction and new_transaction['nonce'] != current_transaction['nonce']:
        raise ValueError('Supplied nonce in new_transaction must match the pending transaction')

    if 'nonce' not in new_transaction:
        new_transaction = assoc(new_transaction, 'nonce', current_transaction['nonce'])

    if 'gasPrice' in new_transaction:
        if new_transaction['gasPrice'] <= current_transaction['gasPrice']:
            raise ValueError('Supplied gas price must exceed existing transaction gas price')
    else:
        generated_gas_price = chain3.mc.generateGasPrice(new_transaction)
        minimum_gas_price = int(math.ceil(current_transaction['gasPrice'] * 1.1))
        if generated_gas_price and generated_gas_price > minimum_gas_price:
            new_transaction = assoc(new_transaction, 'gasPrice', generated_gas_price)
        else:
            new_transaction = assoc(new_transaction, 'gasPrice', minimum_gas_price)

    return new_transaction


def replace_transaction(chain3, current_transaction, new_transaction):
    new_transaction = prepare_replacement_transaction(
        chain3, current_transaction, new_transaction
    )
    return chain3.mc.sendTransaction(new_transaction)
