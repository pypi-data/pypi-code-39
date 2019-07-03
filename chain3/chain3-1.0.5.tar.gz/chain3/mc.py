from mc_account import (
    Account,
)
from mc_utils import (
    apply_to_return_value,
    is_checksum_address,
    is_string,
)
from hexbytes import (
    HexBytes,
)

from chain3.contract import (
    Contract,
)
from chain3.iban import (
    Iban,
)
from chain3.module import (
    Module,
)
from chain3.utils.blocks import (
    select_method_for_block_identifier,
)
from chain3.utils.decorators import (
    deprecated_for,
)
from chain3.utils.empty import (
    empty,
)
from chain3.utils.encoding import (
    to_hex,
)
from chain3.utils.filters import (
    BlockFilter,
    LogFilter,
    TransactionFilter,
)
from chain3.utils.toolz import (
    assoc,
    merge,
)
from chain3.utils.transactions import (
    assert_valid_transaction_params,
    extract_valid_transaction_params,
    get_buffered_gas_estimate,
    get_required_transaction,
    replace_transaction,
    wait_for_transaction_receipt,
)


class MC(Module):
    account = Account()
    defaultAccount = empty
    defaultBlock = "latest"
    defaultContractFactory = Contract
    iban = Iban
    gasPriceStrategy = None

    @deprecated_for("doing nothing at all")
    def enable_unaudited_features(self):
        pass

    def namereg(self):
        raise NotImplementedError()

    def icapNamereg(self):
        raise NotImplementedError()

    @property
    def protocolVersion(self):
        return self.chain3.manager.request_blocking("mc_protocolVersion", [])

    @property
    def syncing(self):
        return self.chain3.manager.request_blocking("mc_syncing", [])

    @property
    def coinbase(self):
        return self.chain3.manager.request_blocking("mc_coinbase", [])

    @property
    def mining(self):
        return self.chain3.manager.request_blocking("mc_mining", [])

    @property
    def hashrate(self):
        return self.chain3.manager.request_blocking("mc_hashrate", [])

    @property
    def gasPrice(self):
        return self.chain3.manager.request_blocking("mc_gasPrice", [])

    @property
    def accounts(self):
        return self.chain3.manager.request_blocking("mc_accounts", [])

    @property
    def blockNumber(self):
        return self.chain3.manager.request_blocking("mc_blockNumber", [])

    def getBalance(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.chain3.manager.request_blocking(
            "mc_getBalance",
            [account, block_identifier],
        )

    def getStorageAt(self, account, position, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.chain3.manager.request_blocking(
            "mc_getStorageAt",
            [account, position, block_identifier]
        )

    def getCode(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.chain3.manager.request_blocking(
            "mc_getCode",
            [account, block_identifier],
        )

    def getBlock(self, block_identifier, full_transactions=False):
        """
        `mc_getBlockByHash`
        `mc_getBlockByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='mc_getBlockByNumber',
            if_hash='mc_getBlockByHash',
            if_number='mc_getBlockByNumber',
        )

        return self.chain3.manager.request_blocking(
            method,
            [block_identifier, full_transactions],
        )

    def getBlockTransactionCount(self, block_identifier):
        """
        `mc_getBlockTransactionCountByHash`
        `mc_getBlockTransactionCountByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='mc_getBlockTransactionCountByNumber',
            if_hash='mc_getBlockTransactionCountByHash',
            if_number='mc_getBlockTransactionCountByNumber',
        )
        return self.chain3.manager.request_blocking(
            method,
            [block_identifier],
        )

    def getUncleCount(self, block_identifier):
        """
        `mc_getUncleCountByBlockHash`
        `mc_getUncleCountByBlockNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='mc_getUncleCountByBlockNumber',
            if_hash='mc_getUncleCountByBlockHash',
            if_number='mc_getUncleCountByBlockNumber',
        )
        return self.chain3.manager.request_blocking(
            method,
            [block_identifier],
        )

    def getUncleByBlock(self, block_identifier, uncle_index):
        """
        `mc_getUncleByBlockHashAndIndex`
        `mc_getUncleByBlockNumberAndIndex`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='mc_getUncleByBlockNumberAndIndex',
            if_hash='mc_getUncleByBlockHashAndIndex',
            if_number='mc_getUncleByBlockNumberAndIndex',
        )
        return self.chain3.manager.request_blocking(
            method,
            [block_identifier, uncle_index],
        )

    def getTransaction(self, transaction_hash):
        return self.chain3.manager.request_blocking(
            "mc_getTransactionByHash",
            [transaction_hash],
        )

    def getTransactionFromBlock(self, block_identifier, transaction_index):
        """
        Alias for the method getTransactionByBlock
        Depreceated to maintain naming consistency with the json-rpc API
        """
        return self.getTransactionByBlock(block_identifier, transaction_index)

    def getTransactionByBlock(self, block_identifier, transaction_index):
        """
        `mc_getTransactionByBlockHashAndIndex`
        `mc_getTransactionByBlockNumberAndIndex`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='mc_getTransactionByBlockNumberAndIndex',
            if_hash='mc_getTransactionByBlockHashAndIndex',
            if_number='mc_getTransactionByBlockNumberAndIndex',
        )
        return self.chain3.manager.request_blocking(
            method,
            [block_identifier, transaction_index],
        )

    def waitForTransactionReceipt(self, transaction_hash, timeout=120):
        return wait_for_transaction_receipt(self.chain3, transaction_hash, timeout)

    def getTransactionReceipt(self, transaction_hash):
        return self.chain3.manager.request_blocking(
            "mc_getTransactionReceipt",
            [transaction_hash],
        )

    def getTransactionCount(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.chain3.manager.request_blocking(
            "mc_getTransactionCount",
            [
                account,
                block_identifier,
            ],
        )

    def replaceTransaction(self, transaction_hash, new_transaction):
        current_transaction = get_required_transaction(self.chain3, transaction_hash)
        return replace_transaction(self.chain3, current_transaction, new_transaction)

    def modifyTransaction(self, transaction_hash, **transaction_params):
        assert_valid_transaction_params(transaction_params)
        current_transaction = get_required_transaction(self.chain3, transaction_hash)
        current_transaction_params = extract_valid_transaction_params(current_transaction)
        new_transaction = merge(current_transaction_params, transaction_params)
        return replace_transaction(self.chain3, current_transaction, new_transaction)

    def sendTransaction(self, transaction):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        # TODO: move gas estimation in middleware
        if 'gas' not in transaction:
            transaction = assoc(
                transaction,
                'gas',
                get_buffered_gas_estimate(self.chain3, transaction),
            )

        # add for subchain
        if 'shardingFlag' not in transaction:
            transaction = assoc(transaction, 'shardingFlag', 0,)
        if 'via' not in transaction:
            transaction = assoc(transaction, 'via', '0x0000000000000000000000000000000000000000',)

        return self.chain3.manager.request_blocking(
            "mc_sendTransaction",
            [transaction],
        )

    def sendRawTransaction(self, raw_transaction):
        return self.chain3.manager.request_blocking(
            "mc_sendRawTransaction",
            [raw_transaction],
        )

    def sign(self, account, data=None, hexstr=None, text=None):
        message_hex = to_hex(data, hexstr=hexstr, text=text)
        return self.chain3.manager.request_blocking(
            "mc_sign", [account, message_hex],
        )

    @apply_to_return_value(HexBytes)
    def call(self, transaction, block_identifier=None):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        # TODO: move to middleware
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.chain3.manager.request_blocking(
            "mc_call",
            [transaction, block_identifier],
        )

    def estimateGas(self, transaction):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        return self.chain3.manager.request_blocking(
            "mc_estimateGas",
            [transaction],
        )

    def filter(self, filter_params=None, filter_id=None):
        if filter_id and filter_params:
            raise TypeError(
                "Ambiguous invocation: provide either a `filter_params` or a `filter_id` argument. "
                "Both were supplied."
            )
        if is_string(filter_params):
            if filter_params == "latest":
                filter_id = self.chain3.manager.request_blocking(
                    "mc_newBlockFilter", [],
                )
                return BlockFilter(self.chain3, filter_id)
            elif filter_params == "pending":
                filter_id = self.chain3.manager.request_blocking(
                    "mc_newPendingTransactionFilter", [],
                )
                return TransactionFilter(self.chain3, filter_id)
            else:
                raise ValueError(
                    "The filter API only accepts the values of `pending` or "
                    "`latest` for string based filters"
                )
        elif isinstance(filter_params, dict):
            _filter_id = self.chain3.manager.request_blocking(
                "mc_newFilter",
                [filter_params],
            )
            return LogFilter(self.chain3, _filter_id)
        elif filter_id and not filter_params:
            return LogFilter(self.chain3, filter_id)
        else:
            raise TypeError("Must provide either filter_params as a string or "
                            "a valid filter object, or a filter_id as a string "
                            "or hex.")

    def getFilterChanges(self, filter_id):
        return self.chain3.manager.request_blocking(
            "mc_getFilterChanges", [filter_id],
        )

    def getFilterLogs(self, filter_id):
        return self.chain3.manager.request_blocking(
            "mc_getFilterLogs", [filter_id],
        )

    def getLogs(self, filter_params):
        return self.chain3.manager.request_blocking(
            "mc_getLogs", [filter_params],
        )

    def uninstallFilter(self, filter_id):
        return self.chain3.manager.request_blocking(
            "mc_uninstallFilter", [filter_id],
        )

    def contract(self,
                 address=None,
                 **kwargs):
        ContractFactoryClass = kwargs.pop('ContractFactoryClass', self.defaultContractFactory)

        ContractFactory = ContractFactoryClass.factory(self.chain3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def setContractFactory(self, contractFactory):
        self.defaultContractFactory = contractFactory

    def getCompilers(self):
        return self.chain3.manager.request_blocking("mc_getCompilers", [])

    def getWork(self):
        return self.chain3.manager.request_blocking("mc_getWork", [])

    def generateGasPrice(self, transaction_params=None):
        if self.gasPriceStrategy:
            return self.gasPriceStrategy(self.chain3, transaction_params)

    def setGasPriceStrategy(self, gas_price_strategy):
        self.gasPriceStrategy = gas_price_strategy
