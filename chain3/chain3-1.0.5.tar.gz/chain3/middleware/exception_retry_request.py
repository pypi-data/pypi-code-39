from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects,
)

whitelist = [
    'admin',
    'shh',
    'miner',
    'net',
    'txpool'
    'testing',
    'evm',
    'mc_protocolVersion',
    'mc_syncing',
    'mc_coinbase',
    'mc_mining',
    'mc_hashrate',
    'mc_gasPrice',
    'mc_accounts',
    'mc_blockNumber',
    'mc_getBalance',
    'mc_getStorageAt',
    'mc_getCode',
    'mc_getBlockByNumber',
    'mc_getBlockByHash',
    'mc_getBlockTransactionCountByNumber',
    'mc_getBlockTransactionCountByHash',
    'mc_getUncleCountByBlockNumber',
    'mc_getUncleCountByBlockHash',
    'mc_getTransactionByHash',
    'mc_getTransactionByBlockHashAndIndex',
    'mc_getTransactionByBlockNumberAndIndex',
    'mc_getTransactionReceipt',
    'mc_getTransactionCount',
    'mc_call',
    'mc_estimateGas',
    'mc_newBlockFilter',
    'mc_newPendingTransactionFilter',
    'mc_newFilter',
    'mc_getFilterChanges',
    'mc_getFilterLogs',
    'mc_getLogs',
    'mc_uninstallFilter',
    'mc_getCompilers',
    'mc_getWork',
    'mc_sign',
    'mc_sendRawTransaction',
    'personal_importRawKey',
    'personal_newAccount',
    'personal_listAccounts',
    'personal_lockAccount',
    'personal_unlockAccount',
    'personal_ecRecover',
    'personal_sign'
]


def check_if_retry_on_failure(method):
    root = method.split('_')[0]
    if root in whitelist:
        return True
    elif method in whitelist:
        return True
    else:
        return False


def exception_retry_middleware(make_request, chain3, errors, retries=5):
    '''
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    '''
    def middleware(method, params):
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                except errors:
                    if i < retries - 1:
                        continue
                    else:
                        raise
        else:
            return make_request(method, params)
    return middleware


def http_retry_request_middleware(make_request, chain3):
    return exception_retry_middleware(
        make_request,
        chain3,
        (ConnectionError, HTTPError, Timeout, TooManyRedirects)
    )
