from mc_utils import (
    is_checksum_address,
    is_list_like,
    is_same_address,
)

PRIVATE_KEY_HEX = '0x56ebb41875ceedd42e395f730e03b5c44989393c9f0484ee6bc05f933673458f'
PASSWORD = 'chain3-testing'
ADDRESS = '0x844B417c0C58B02c2224306047B9fb0D3264fE8c'


PRIVATE_KEY_FOR_UNLOCK = '0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01'
ACCOUNT_FOR_UNLOCK = '0x12efDc31B1a8FA1A1e756DFD8A1601055C971E13'


class PersonalModuleTest:
    def test_personal_importRawKey(self, chain3):
        actual = chain3.personal.importRawKey(PRIVATE_KEY_HEX, PASSWORD)
        assert actual == ADDRESS

    def test_personal_listAccounts(self, chain3):
        accounts = chain3.personal.listAccounts
        assert is_list_like(accounts)
        assert len(accounts) > 0
        assert all((
            is_checksum_address(item)
            for item
            in accounts
        ))

    def test_personal_lockAccount(self, chain3, unlocked_account):
        # TODO: how do we test this better?
        chain3.personal.lockAccount(unlocked_account)

    def test_personal_unlockAccount_success(self,
                                            chain3,
                                            unlockable_account,
                                            unlockable_account_pw):
        result = chain3.personal.unlockAccount(unlockable_account, unlockable_account_pw)
        assert result is True

    def test_personal_unlockAccount_failure(self,
                                            chain3,
                                            unlockable_account):
        result = chain3.personal.unlockAccount(unlockable_account, 'bad-password')
        assert result is False

    def test_personal_newAccount(self, chain3):
        new_account = chain3.personal.newAccount(PASSWORD)
        assert is_checksum_address(new_account)

    def test_personal_sendTransaction(self,
                                      chain3,
                                      unlockable_account,
                                      unlockable_account_pw):
        assert chain3.mc.getBalance(unlockable_account) > chain3.toWei(1, 'ether')
        txn_params = {
            'from': unlockable_account,
            'to': unlockable_account,
            'gas': 21000,
            'value': 1,
            'gasPrice': chain3.toWei(1, 'gwei'),
        }
        txn_hash = chain3.personal.sendTransaction(txn_params, unlockable_account_pw)
        assert txn_hash
        transaction = chain3.mc.getTransaction(txn_hash)
        assert transaction['from'] == txn_params['from']
        assert transaction['to'] == txn_params['to']
        assert transaction['gas'] == txn_params['gas']
        assert transaction['value'] == txn_params['value']
        assert transaction['gasPrice'] == txn_params['gasPrice']

    def test_personal_sign_and_ecrecover(self,
                                         chain3,
                                         unlockable_account,
                                         unlockable_account_pw):
        message = 'test-chain3-personal-sign'
        signature = chain3.personal.sign(message, unlockable_account, unlockable_account_pw)
        signer = chain3.personal.ecRecover(message, signature)
        assert is_same_address(signer, unlockable_account)
