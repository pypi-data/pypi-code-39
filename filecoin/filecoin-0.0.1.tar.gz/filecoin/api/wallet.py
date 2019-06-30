# coding: utf8
from filecoin.utils import run_filecoin_cmd



def get_addresses():
    addresses = run_filecoin_cmd('address ls', split_into_lines=True)
    return addresses


def get_default_address():
    default_address = run_filecoin_cmd('address default').strip()
    return default_address

def create_new_address():
    new_address = run_filecoin_cmd('address new').strip()
    return new_address



def get_balance():
    balance = {}
    addresses = get_addresses()
    for address in addresses:
        address_balance = run_filecoin_cmd('wallet balance %s' % address)
        try:
            address_balance = int(address_balance.strip())
            balance[address] = address_balance
        except:
            pass
    return balance



def backup_wallet():
    pass