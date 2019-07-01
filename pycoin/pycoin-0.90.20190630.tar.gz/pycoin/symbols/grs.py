from pycoin.coins.groestlcoin.hash import groestlHash
from pycoin.coins.groestlcoin.parse import GRSParseAPI
from pycoin.coins.groestlcoin.Block import Block as GrsBlock
from pycoin.coins.groestlcoin.Tx import Tx as GrsTx
from pycoin.encoding.b58 import b2a_base58
from pycoin.encoding.hexbytes import h2b
from pycoin.networks.bitcoinish import create_bitcoinish_network


network = create_bitcoinish_network(
    symbol="GRS", network_name="Groestlcoin", subnet_name="mainnet", tx=GrsTx, block=GrsBlock,
    wif_prefix_hex="80", sec_prefix="GRSSEC:", address_prefix_hex="24", pay_to_script_prefix_hex="05",
    bip32_prv_prefix_hex="0488ade4", bip32_pub_prefix_hex="0488B21E", bech32_hrp="grs",
    magic_header_hex="F9BEB4D9", default_port=1331,
    parse_api_class=GRSParseAPI,
    dns_bootstrap=[
        "groestlcoin.org", "electrum1.groestlcoin.org", "electrum2.groestlcoin.org",
        "jswallet.groestlcoin.org", "groestlsight.groestlcoin.org"
    ]
)

# monkey patches
_wif_prefix = h2b("80")
_bip32_prv_prefix = h2b("0488ade4")
_bip32_pub_prefix = h2b("0488B21E")


def b2a_hashed_base58_grs(data):
    return b2a_base58(data + groestlHash(data)[:4])


def bip32_as_string(blob, as_private):
    prefix = _bip32_prv_prefix if as_private else _bip32_pub_prefix
    return b2a_hashed_base58_grs(prefix + blob)


def wif_for_blob(blob):
    return b2a_hashed_base58_grs(_wif_prefix + blob)


network.address.b2a = b2a_hashed_base58_grs
network.bip32_as_string = bip32_as_string
network.wif_for_blob = wif_for_blob

# Cause parsing to fail and tests to skip.
try:
    import groestlcoin_hash  # noqa
except ImportError:
    network.Key = None

    def none_parser(*args, **kwargs):
        return None

    for attr in "hierarchical_key private_key public_key address".split():
        setattr(network.parse, attr, none_parser)
