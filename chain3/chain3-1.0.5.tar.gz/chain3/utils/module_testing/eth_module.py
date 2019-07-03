# -*- coding: utf-8 -*-

import pytest

from mc_abi import (
    decode_single,
)
from mc_utils import (
    is_boolean,
    is_bytes,
    is_checksum_address,
    is_dict,
    is_integer,
    is_list_like,
    is_same_address,
    is_string,
)
from hexbytes import (
    HexBytes,
)

from chain3.exceptions import (
    InvalidAddress,
)

UNKNOWN_ADDRESS = '0xdeadbeef00000000000000000000000000000000'
UNKNOWN_HASH = '0xdeadbeef00000000000000000000000000000000000000000000000000000000'


class EthModuleTest:
    def test_mc_protocolVersion(self, chain3):
        protocol_version = chain3.version.ethereum

        assert is_string(protocol_version)
        assert protocol_version.isdigit()

    def test_mc_syncing(self, chain3):
        syncing = chain3.mc.syncing

        assert is_boolean(syncing) or is_dict(syncing)

        if is_boolean(syncing):
            assert syncing is False
        elif is_dict(syncing):
            assert 'startingBlock' in syncing
            assert 'currentBlock' in syncing
            assert 'highestBlock' in syncing

            assert is_integer(syncing['startingBlock'])
            assert is_integer(syncing['currentBlock'])
            assert is_integer(syncing['highestBlock'])

    def test_mc_coinbase(self, chain3):
        coinbase = chain3.mc.coinbase
        assert is_checksum_address(coinbase)

    def test_mc_mining(self, chain3):
        mining = chain3.mc.mining
        assert is_boolean(mining)

    def test_mc_hashrate(self, chain3):
        hashrate = chain3.mc.hashrate
        assert is_integer(hashrate)
        assert hashrate >= 0

    def test_mc_gasPrice(self, chain3):
        gas_price = chain3.mc.gasPrice
        assert is_integer(gas_price)
        assert gas_price > 0

    def test_mc_accounts(self, chain3):
        accounts = chain3.mc.accounts
        assert is_list_like(accounts)
        assert len(accounts) != 0
        assert all((
            is_checksum_address(account)
            for account
            in accounts
        ))
        assert chain3.mc.coinbase in accounts

    def test_mc_blockNumber(self, chain3):
        block_number = chain3.mc.blockNumber
        assert is_integer(block_number)
        assert block_number >= 0

    def test_mc_getBalance(self, chain3):
        coinbase = chain3.mc.coinbase

        with pytest.raises(InvalidAddress):
            chain3.mc.getBalance(coinbase.lower())

        balance = chain3.mc.getBalance(coinbase)

        assert is_integer(balance)
        assert balance >= 0

    def test_mc_getStorageAt(self, chain3):
        coinbase = chain3.mc.coinbase

        with pytest.raises(InvalidAddress):
            chain3.mc.getStorageAt(coinbase.lower(), 0)

    def test_mc_getTransactionCount(self, chain3):
        coinbase = chain3.mc.coinbase
        transaction_count = chain3.mc.getTransactionCount(coinbase)
        with pytest.raises(InvalidAddress):
            chain3.mc.getTransactionCount(coinbase.lower())

        assert is_integer(transaction_count)
        assert transaction_count >= 0

    def test_mc_getBlockTransactionCountByHash_empty_block(self, chain3, empty_block):
        transaction_count = chain3.mc.getBlockTransactionCount(empty_block['hash'])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_mc_getBlockTransactionCountByNumber_empty_block(self, chain3, empty_block):
        transaction_count = chain3.mc.getBlockTransactionCount(empty_block['number'])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_mc_getBlockTransactionCountByHash_block_with_txn(self, chain3, block_with_txn):
        transaction_count = chain3.mc.getBlockTransactionCount(block_with_txn['hash'])

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    def test_mc_getBlockTransactionCountByNumber_block_with_txn(self, chain3, block_with_txn):
        transaction_count = chain3.mc.getBlockTransactionCount(block_with_txn['number'])

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    def test_mc_getUncleCountByBlockHash(self, chain3, empty_block):
        uncle_count = chain3.mc.getUncleCount(empty_block['hash'])

        assert is_integer(uncle_count)
        assert uncle_count == 0

    def test_mc_getUncleCountByBlockNumber(self, chain3, empty_block):
        uncle_count = chain3.mc.getUncleCount(empty_block['number'])

        assert is_integer(uncle_count)
        assert uncle_count == 0

    def test_mc_getCode(self, chain3, math_contract):
        code = chain3.mc.getCode(math_contract.address)
        with pytest.raises(InvalidAddress):
            code = chain3.mc.getCode(math_contract.address.lower())
        assert is_string(code)
        assert len(code) > 2

    def test_mc_sign(self, chain3, unlocked_account):
        signature = chain3.mc.sign(unlocked_account, text='Message tö sign. Longer than hash!')
        assert is_bytes(signature)
        assert len(signature) == 32 + 32 + 1

        # test other formats
        hexsign = chain3.mc.sign(
            unlocked_account,
            hexstr='0x4d6573736167652074c3b6207369676e2e204c6f6e676572207468616e206861736821'
        )
        assert hexsign == signature

        intsign = chain3.mc.sign(
            unlocked_account,
            0x4d6573736167652074c3b6207369676e2e204c6f6e676572207468616e206861736821
        )
        assert intsign == signature

        bytessign = chain3.mc.sign(unlocked_account, b'Message t\xc3\xb6 sign. Longer than hash!')
        assert bytessign == signature

        new_signature = chain3.mc.sign(unlocked_account, text='different message is different')
        assert new_signature != signature

    def test_mc_sendTransaction_addr_checksum_required(self, chain3, unlocked_account):
        non_checksum_addr = unlocked_account.lower()
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }

        with pytest.raises(InvalidAddress):
            invalid_params = dict(txn_params, **{'from': non_checksum_addr})
            chain3.mc.sendTransaction(invalid_params)

        with pytest.raises(InvalidAddress):
            invalid_params = dict(txn_params, **{'to': non_checksum_addr})
            chain3.mc.sendTransaction(invalid_params)

    def test_mc_sendTransaction(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)
        txn = chain3.mc.getTransaction(txn_hash)

        assert is_same_address(txn['from'], txn_params['from'])
        assert is_same_address(txn['to'], txn_params['to'])
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['gasPrice'] == txn_params['gasPrice']

    def test_mc_sendTransaction_with_nonce(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            # Increased gas price to ensure transaction hash different from other tests
            'gasPrice': chain3.mc.gasPrice * 2,
            'nonce': chain3.mc.getTransactionCount(unlocked_account),
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)
        txn = chain3.mc.getTransaction(txn_hash)

        assert is_same_address(txn['from'], txn_params['from'])
        assert is_same_address(txn['to'], txn_params['to'])
        assert txn['value'] == 1
        assert txn['gas'] == 21000
        assert txn['gasPrice'] == txn_params['gasPrice']
        assert txn['nonce'] == txn_params['nonce']

    def test_mc_replaceTransaction(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        txn_params['gasPrice'] = chain3.mc.gasPrice * 2
        replace_txn_hash = chain3.mc.replaceTransaction(txn_hash, txn_params)
        replace_txn = chain3.mc.getTransaction(replace_txn_hash)

        assert is_same_address(replace_txn['from'], txn_params['from'])
        assert is_same_address(replace_txn['to'], txn_params['to'])
        assert replace_txn['value'] == 1
        assert replace_txn['gas'] == 21000
        assert replace_txn['gasPrice'] == txn_params['gasPrice']

    def test_mc_replaceTransaction_non_existing_transaction(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }
        with pytest.raises(ValueError):
            chain3.mc.replaceTransaction(
                '0x98e8cc09b311583c5079fa600f6c2a3bea8611af168c52e4b60b5b243a441997',
                txn_params
            )

    # auto mine is enabled for this test
    def test_mc_replaceTransaction_already_mined(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        txn_params['gasPrice'] = chain3.mc.gasPrice * 2
        with pytest.raises(ValueError):
            chain3.mc.replaceTransaction(txn_hash, txn_params)

    def test_mc_replaceTransaction_incorrect_nonce(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)
        txn = chain3.mc.getTransaction(txn_hash)

        txn_params['gasPrice'] = chain3.mc.gasPrice * 2
        txn_params['nonce'] = txn['nonce'] + 1
        with pytest.raises(ValueError):
            chain3.mc.replaceTransaction(txn_hash, txn_params)

    def test_mc_replaceTransaction_gas_price_too_low(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': 10,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        txn_params['gasPrice'] = 9
        with pytest.raises(ValueError):
            chain3.mc.replaceTransaction(txn_hash, txn_params)

    def test_mc_replaceTransaction_gas_price_defaulting_minimum(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': 10,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        txn_params.pop('gasPrice')
        replace_txn_hash = chain3.mc.replaceTransaction(txn_hash, txn_params)
        replace_txn = chain3.mc.getTransaction(replace_txn_hash)

        assert replace_txn['gasPrice'] == 11  # minimum gas price

    def test_mc_replaceTransaction_gas_price_defaulting_strategy_higher(self,
                                                                         chain3,
                                                                         unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': 10,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        def higher_gas_price_strategy(chain3, txn):
            return 20

        chain3.mc.setGasPriceStrategy(higher_gas_price_strategy)

        txn_params.pop('gasPrice')
        replace_txn_hash = chain3.mc.replaceTransaction(txn_hash, txn_params)
        replace_txn = chain3.mc.getTransaction(replace_txn_hash)
        assert replace_txn['gasPrice'] == 20  # Strategy provides higher gas price

    def test_mc_replaceTransaction_gas_price_defaulting_strategy_lower(self,
                                                                        chain3,
                                                                        unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': 10,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        def lower_gas_price_strategy(chain3, txn):
            return 5

        chain3.mc.setGasPriceStrategy(lower_gas_price_strategy)

        txn_params.pop('gasPrice')
        replace_txn_hash = chain3.mc.replaceTransaction(txn_hash, txn_params)
        replace_txn = chain3.mc.getTransaction(replace_txn_hash)
        # Strategy provices lower gas price - minimum preferred
        assert replace_txn['gasPrice'] == 11

    def test_mc_modifyTransaction(self, chain3, unlocked_account):
        txn_params = {
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        }
        txn_hash = chain3.mc.sendTransaction(txn_params)

        modified_txn_hash = chain3.mc.modifyTransaction(
            txn_hash, gasPrice=(txn_params['gasPrice'] * 2), value=2
        )
        modified_txn = chain3.mc.getTransaction(modified_txn_hash)

        assert is_same_address(modified_txn['from'], txn_params['from'])
        assert is_same_address(modified_txn['to'], txn_params['to'])
        assert modified_txn['value'] == 2
        assert modified_txn['gas'] == 21000
        assert modified_txn['gasPrice'] == txn_params['gasPrice'] * 2

    @pytest.mark.parametrize(
        'raw_transaction, expected_hash',
        [
            (
                # address 0x39EEed73fb1D3855E90Cbd42f348b3D7b340aAA6
                '0xf8648085174876e8008252089439eeed73fb1d3855e90cbd42f348b3d7b340aaa601801ba0ec1295f00936acd0c2cb90ab2cdaacb8bf5e11b3d9957833595aca9ceedb7aada05dfc8937baec0e26029057abd3a1ef8c505dca2cdc07ffacb046d090d2bea06a',  # noqa: E501
                '0x1f80f8ab5f12a45be218f76404bda64d37270a6f4f86ededd0eb599f80548c13',
            ),
            (
                # private key 0x3c2ab4e8f17a7dea191b8c991522660126d681039509dc3bb31af7c9bdb63518
                # This is an unfunded account, but the transaction has a 0 gas price, so is valid.
                # It never needs to be mined, we just want the transaction hash back to confirm.
                HexBytes('0xf85f808082c35094d898d5e829717c72e7438bad593076686d7d164a80801ba005c2e99ecee98a12fbf28ab9577423f42e9e88f2291b3acc8228de743884c874a077d6bc77a47ad41ec85c96aac2ad27f05a039c4787fca8a1e5ee2d8c7ec1bb6a'),  # noqa: E501
                '0x98eeadb99454427f6aad7b558bac13e9d225512a6f5e5c11cf48e8d4067e51b5',
            ),
        ]
    )
    def test_mc_sendRawTransaction(self,
                                    chain3,
                                    raw_transaction,
                                    funded_account_for_raw_txn,
                                    expected_hash):
        txn_hash = chain3.mc.sendRawTransaction(raw_transaction)
        assert txn_hash == chain3.toBytes(hexstr=expected_hash)

    def test_mc_call(self, chain3, math_contract):
        coinbase = chain3.mc.coinbase
        txn_params = math_contract._prepare_transaction(
            fn_name='add',
            fn_args=(7, 11),
            transaction={'from': coinbase, 'to': math_contract.address},
        )
        call_result = chain3.mc.call(txn_params)
        assert is_string(call_result)
        result = decode_single('uint256', call_result)
        assert result == 18

    def test_mc_call_with_0_result(self, chain3, math_contract):
        coinbase = chain3.mc.coinbase
        txn_params = math_contract._prepare_transaction(
            fn_name='add',
            fn_args=(0, 0),
            transaction={'from': coinbase, 'to': math_contract.address},
        )
        call_result = chain3.mc.call(txn_params)
        assert is_string(call_result)
        result = decode_single('uint256', call_result)
        assert result == 0

    def test_mc_estimateGas(self, chain3):
        coinbase = chain3.mc.coinbase
        gas_estimate = chain3.mc.estimateGas({
            'from': coinbase,
            'to': coinbase,
            'value': 1,
        })
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    def test_mc_getBlockByHash(self, chain3, empty_block):
        block = chain3.mc.getBlock(empty_block['hash'])
        assert block['hash'] == empty_block['hash']

    def test_mc_getBlockByHash_not_found(self, chain3, empty_block):
        block = chain3.mc.getBlock(UNKNOWN_HASH)
        assert block is None

    def test_mc_getBlockByNumber_with_integer(self, chain3, empty_block):
        block = chain3.mc.getBlock(empty_block['number'])
        assert block['number'] == empty_block['number']

    def test_mc_getBlockByNumber_latest(self, chain3, empty_block):
        current_block_number = chain3.mc.blockNumber
        block = chain3.mc.getBlock('latest')
        assert block['number'] == current_block_number

    def test_mc_getBlockByNumber_not_found(self, chain3, empty_block):
        block = chain3.mc.getBlock(12345)
        assert block is None

    def test_mc_getBlockByNumber_pending(self, chain3, empty_block):
        current_block_number = chain3.mc.blockNumber
        block = chain3.mc.getBlock('pending')
        assert block['number'] == current_block_number + 1

    def test_mc_getBlockByNumber_earliest(self, chain3, empty_block):
        genesis_block = chain3.mc.getBlock(0)
        block = chain3.mc.getBlock('earliest')
        assert block['number'] == 0
        assert block['hash'] == genesis_block['hash']

    def test_mc_getBlockByNumber_full_transactions(self, chain3, block_with_txn):
        block = chain3.mc.getBlock(block_with_txn['number'], True)
        transaction = block['transactions'][0]
        assert transaction['hash'] == block_with_txn['transactions'][0]

    def test_mc_getTransactionByHash(self, chain3, mined_txn_hash):
        transaction = chain3.mc.getTransaction(mined_txn_hash)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_mc_getTransactionByHash_contract_creation(self,
                                                        chain3,
                                                        math_contract_deploy_txn_hash):
        transaction = chain3.mc.getTransaction(math_contract_deploy_txn_hash)
        assert is_dict(transaction)
        assert transaction['to'] is None, "to field is %r" % transaction['to']

    def test_mc_getTransactionFromBlockHashAndIndex(self, chain3, block_with_txn, mined_txn_hash):
        transaction = chain3.mc.getTransactionFromBlock(block_with_txn['hash'], 0)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_mc_getTransactionFromBlockNumberAndIndex(self, chain3, block_with_txn, mined_txn_hash):
        transaction = chain3.mc.getTransactionFromBlock(block_with_txn['number'], 0)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_mc_getTransactionByBlockHashAndIndex(self, chain3, block_with_txn, mined_txn_hash):
        transaction = chain3.mc.getTransactionByBlock(block_with_txn['hash'], 0)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_mc_getTransactionByBlockNumberAndIndex(self, chain3, block_with_txn, mined_txn_hash):
        transaction = chain3.mc.getTransactionByBlock(block_with_txn['number'], 0)
        assert is_dict(transaction)
        assert transaction['hash'] == HexBytes(mined_txn_hash)

    def test_mc_getTransactionReceipt_mined(self, chain3, block_with_txn, mined_txn_hash):
        receipt = chain3.mc.getTransactionReceipt(mined_txn_hash)
        assert is_dict(receipt)
        assert receipt['blockNumber'] == block_with_txn['number']
        assert receipt['blockHash'] == block_with_txn['hash']
        assert receipt['transactionIndex'] == 0
        assert receipt['transactionHash'] == HexBytes(mined_txn_hash)

    def test_mc_getTransactionReceipt_unmined(self, chain3, unlocked_account):
        txn_hash = chain3.mc.sendTransaction({
            'from': unlocked_account,
            'to': unlocked_account,
            'value': 1,
            'gas': 21000,
            'gasPrice': chain3.mc.gasPrice,
        })
        receipt = chain3.mc.getTransactionReceipt(txn_hash)
        assert receipt is None

    def test_mc_getTransactionReceipt_with_log_entry(self,
                                                      chain3,
                                                      block_with_txn_with_log,
                                                      emitter_contract,
                                                      txn_hash_with_log):
        receipt = chain3.mc.getTransactionReceipt(txn_hash_with_log)
        assert is_dict(receipt)
        assert receipt['blockNumber'] == block_with_txn_with_log['number']
        assert receipt['blockHash'] == block_with_txn_with_log['hash']
        assert receipt['transactionIndex'] == 0
        assert receipt['transactionHash'] == HexBytes(txn_hash_with_log)

        assert len(receipt['logs']) == 1
        log_entry = receipt['logs'][0]

        assert log_entry['blockNumber'] == block_with_txn_with_log['number']
        assert log_entry['blockHash'] == block_with_txn_with_log['hash']
        assert log_entry['logIndex'] == 0
        assert is_same_address(log_entry['address'], emitter_contract.address)
        assert log_entry['transactionIndex'] == 0
        assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

    def test_mc_getUncleByBlockHashAndIndex(self, chain3):
        # TODO: how do we make uncles....
        pass

    def test_mc_getUncleByBlockNumberAndIndex(self, chain3):
        # TODO: how do we make uncles....
        pass

    def test_mc_getCompilers(self, chain3):
        # TODO: do we want to test this?
        pass

    def test_mc_compileSolidity(self, chain3):
        # TODO: do we want to test this?
        pass

    def test_mc_compileLLL(self, chain3):
        # TODO: do we want to test this?
        pass

    def test_mc_compileSerpent(self, chain3):
        # TODO: do we want to test this?
        pass

    def test_mc_newFilter(self, chain3):
        filter = chain3.mc.filter({})

        changes = chain3.mc.getFilterChanges(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        logs = chain3.mc.getFilterLogs(filter.filter_id)
        assert is_list_like(logs)
        assert not logs

        result = chain3.mc.uninstallFilter(filter.filter_id)
        assert result is True

    def test_mc_newBlockFilter(self, chain3):
        filter = chain3.mc.filter('latest')
        assert is_string(filter.filter_id)

        changes = chain3.mc.getFilterChanges(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        # TODO: figure out why this fails in go-ethereum
        # logs = chain3.mc.getFilterLogs(filter.filter_id)
        # assert is_list_like(logs)
        # assert not logs

        result = chain3.mc.uninstallFilter(filter.filter_id)
        assert result is True

    def test_mc_newPendingTransactionFilter(self, chain3):
        filter = chain3.mc.filter('pending')
        assert is_string(filter.filter_id)

        changes = chain3.mc.getFilterChanges(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        # TODO: figure out why this fails in go-ethereum
        # logs = chain3.mc.getFilterLogs(filter.filter_id)
        # assert is_list_like(logs)
        # assert not logs

        result = chain3.mc.uninstallFilter(filter.filter_id)
        assert result is True

    def test_mc_getLogs_without_logs(self, chain3, block_with_txn_with_log):
        # Test with block range

        filter_params = {
            "fromBlock": 0,
            "toBlock": block_with_txn_with_log['number'] - 1,
        }
        result = chain3.mc.getLogs(filter_params)
        assert len(result) == 0

        # the range is wrong
        filter_params = {
            "fromBlock": block_with_txn_with_log['number'],
            "toBlock": block_with_txn_with_log['number'] - 1,
        }
        result = chain3.mc.getLogs(filter_params)
        assert len(result) == 0

        # Test with `address`

        # filter with other address
        filter_params = {
            "fromBlock": 0,
            "address": UNKNOWN_ADDRESS,
        }
        result = chain3.mc.getLogs(filter_params)
        assert len(result) == 0

    def test_mc_getLogs_with_logs(
            self,
            chain3,
            block_with_txn_with_log,
            emitter_contract,
            txn_hash_with_log):

        def assert_contains_log(result):
            assert len(result) == 1
            log_entry = result[0]
            assert log_entry['blockNumber'] == block_with_txn_with_log['number']
            assert log_entry['blockHash'] == block_with_txn_with_log['hash']
            assert log_entry['logIndex'] == 0
            assert is_same_address(log_entry['address'], emitter_contract.address)
            assert log_entry['transactionIndex'] == 0
            assert log_entry['transactionHash'] == HexBytes(txn_hash_with_log)

        # Test with block range

        # the range includes the block where the log resides in
        filter_params = {
            "fromBlock": block_with_txn_with_log['number'],
            "toBlock": block_with_txn_with_log['number'],
        }
        result = chain3.mc.getLogs(filter_params)
        assert_contains_log(result)

        # specify only `from_block`. by default `to_block` should be 'latest'
        filter_params = {
            "fromBlock": 0,
        }
        result = chain3.mc.getLogs(filter_params)
        assert_contains_log(result)

        # Test with `address`

        # filter with emitter_contract.address
        filter_params = {
            "fromBlock": 0,
            "address": emitter_contract.address,
        }
        result = chain3.mc.getLogs(filter_params)
        assert_contains_log(result)

    def test_mc_call_old_contract_state(self, chain3, math_contract, unlocked_account):
        start_block = chain3.mc.getBlock('latest')
        block_num = start_block.number
        block_hash = start_block.hash

        math_contract.functions.increment().transact({'from': unlocked_account})

        # This isn't an incredibly convincing test since we can't mine, and
        # the default resolved block is latest, So if block_identifier was ignored
        # we would get the same result. For now, we mostly depend on core tests.
        # Ideas to improve this test:
        #  - Enable on-demand mining in more clients
        #  - Increment the math contract in all of the fixtures, and check the value in an old block
        block_hash_call_result = math_contract.functions.counter().call(block_identifier=block_hash)
        block_num_call_result = math_contract.functions.counter().call(block_identifier=block_num)
        latest_call_result = math_contract.functions.counter().call(block_identifier='latest')
        default_call_result = math_contract.functions.counter().call()
        pending_call_result = math_contract.functions.counter().call(block_identifier='pending')

        assert block_hash_call_result == 0
        assert block_num_call_result == 0
        assert latest_call_result == 0
        assert default_call_result == 0

        if pending_call_result != 1:
            raise AssertionError("pending call result was %d instead of 1" % pending_call_result)

    def test_mc_uninstallFilter(self, chain3):
        filter = chain3.mc.filter({})
        assert is_string(filter.filter_id)

        success = chain3.mc.uninstallFilter(filter.filter_id)
        assert success is True

        failure = chain3.mc.uninstallFilter(filter.filter_id)
        assert failure is False
