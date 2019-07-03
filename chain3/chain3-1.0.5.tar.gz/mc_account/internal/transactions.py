import itertools

from cytoolz import (
    curry,
    dissoc,
    identity,
    merge,
    partial,
    pipe,
)
from mc_rlp import (
    HashableRLP,
)
from mc_utils.curried import (
    apply_formatters_to_dict,
    apply_one_of_formatters,
    hexstr_if_str,
    is_0x_prefixed,
    is_bytes,
    is_checksum_address,
    is_integer,
    is_string,
    to_bytes,
    to_int,
    to_hex,
)
import rlp
from rlp.sedes import (
    Binary,
    big_endian_int,
    binary,
)


def serializable_unsigned_transaction_from_dict(transaction_dict):
    assert_valid_fields(transaction_dict)
    filled_transaction = pipe(
        transaction_dict,
        dict,
        partial(merge, TRANSACTION_DEFAULTS),
        chain_id_to_v,
        apply_formatters_to_dict(TRANSACTION_FORMATTERS),
    )
    #print('************filled_transaction**************', filled_transaction)
    if 'v' in filled_transaction:
        serializer = Transaction
    else:
        serializer = UnsignedTransaction
    return serializer.from_dict(filled_transaction)


def encode_transaction(unsigned_transaction, vrs):
    (v, r, s) = vrs
    chain_naive_transaction = dissoc(unsigned_transaction.as_dict(), 'v', 'r', 's')
    signed_transaction = Transaction(v=v, r=r, s=s, **chain_naive_transaction)
    #print('************signed_transaction**************', dir(signed_transaction))
    return rlp.encode(signed_transaction)


def is_int_or_prefixed_hexstr(val):
    if is_integer(val):
        return True
    elif isinstance(val, str) and is_0x_prefixed(val):
        return True
    else:
        return False


def is_empty_or_checksum_address(val):
    if val in {None, b'', ''}:
        return True
    elif is_checksum_address(val):
        return True
    else:
        return False


def is_none(val):
    return val is None


TRANSACTION_DEFAULTS = {
    'to': b'',
    'value': 0,
    'data': b'',
    'chainId': None,
    'gasLimit': 0,
    'systemContract': '0x',
    'shardingFlag': 0,
    'via': '0x0000000000000000000000000000000000000000',
}

TRANSACTION_FORMATTERS = {
    'nonce': hexstr_if_str(to_int),
    'gasPrice': hexstr_if_str(to_int),
    'gas': hexstr_if_str(to_int),
    'to': apply_one_of_formatters((
        (is_string, hexstr_if_str(to_bytes)),
        (is_bytes, identity),
        (is_none, lambda val: b''),
    )),
    'value': hexstr_if_str(to_int),
    'data': hexstr_if_str(to_bytes),
    'v': hexstr_if_str(to_int),
    'r': hexstr_if_str(to_int),
    's': hexstr_if_str(to_int),
    'gasLimit': hexstr_if_str(to_int),
    'systemContract': hexstr_if_str(to_bytes),
    'shardingFlag': hexstr_if_str(to_int),     # add  for subchain
    'via': apply_one_of_formatters((
        (is_string, hexstr_if_str(to_bytes)),
        (is_bytes, identity),
        (is_none, lambda val: b''),
    )),        # add for subchain
}

RAW_TRANSACTION_FORMATTERS = {
    'nonce': hexstr_if_str(to_hex),
    'gasPrice': hexstr_if_str(to_hex),
    'to': apply_one_of_formatters((
        (is_string, hexstr_if_str(to_hex)),
        (is_bytes, identity),
        (is_none, lambda val: b''),
    )),
    'value': hexstr_if_str(to_hex),
    'data': hexstr_if_str(to_hex),
    'v': hexstr_if_str(to_hex),
    'r': hexstr_if_str(to_hex),
    's': hexstr_if_str(to_hex),
    'gasLimit': hexstr_if_str(to_hex),
    'systemContract': hexstr_if_str(to_hex),
    'shardingFlag': hexstr_if_str(to_hex),     # add  for subchain
    'via': apply_one_of_formatters((
        (is_string, hexstr_if_str(to_hex)),
        (is_bytes, identity),
        (is_none, lambda val: b''),
    )),        # add for subchain
}

TRANSACTION_VALID_VALUES = {
    'nonce': is_int_or_prefixed_hexstr,
    'gasPrice': is_int_or_prefixed_hexstr,
    'gas': is_int_or_prefixed_hexstr,
    'to': is_empty_or_checksum_address,
    'value': is_int_or_prefixed_hexstr,
    'data': lambda val: isinstance(val, (int, str, bytes, bytearray)),
    'gasLimit': is_int_or_prefixed_hexstr,
    'chainId': lambda val: val is None or is_int_or_prefixed_hexstr(val),
    'systemContract': lambda val: isinstance(val, (int, str, bytes, bytearray)),
    'shardingFlag': is_int_or_prefixed_hexstr,   # add for subchain
    'via': lambda val: isinstance(val, (int, str, bytes, bytearray)),        # add for subchain
}

ALLOWED_TRANSACTION_KEYS = {
    'nonce',
    'gasPrice',
    'to',
    'value',
    'data',
    'gasLimit',
    'chainId',  # set chainId to None if you want a transaction that can be replayed across networks
    'systemContract',
    'shardingFlag',  # add by Michael for subchain
    'via',  # add by Michael for subchain

}

REQUIRED_TRANSACITON_KEYS = ALLOWED_TRANSACTION_KEYS.difference(TRANSACTION_DEFAULTS.keys())


def assert_valid_fields(transaction_dict):
    # check if any keys are missing
    missing_keys = REQUIRED_TRANSACITON_KEYS.difference(transaction_dict.keys())
    if missing_keys:
        raise TypeError("Transaction must include these fields: %r" % missing_keys)

    # check if any extra keys were specified
    superfluous_keys = set(transaction_dict.keys()).difference(ALLOWED_TRANSACTION_KEYS)
    if superfluous_keys:
        raise TypeError("Transaction must not include unrecognized fields: %r" % superfluous_keys)

    # check for valid types in each field
    valid_fields = apply_formatters_to_dict(TRANSACTION_VALID_VALUES, transaction_dict)
    if not all(valid_fields.values()):
        invalid = {key: transaction_dict[key] for key, valid in valid_fields.items() if not valid}
        raise TypeError("Transaction had invalid fields: %r" % invalid)


def chain_id_to_v(transaction_dict):
    # See EIP 155
    chain_id = transaction_dict.pop('chainId')
    if chain_id is None:
        return transaction_dict
    else:
        return dict(transaction_dict, v=chain_id, r=0, s=0)


@curry
def fill_transaction_defaults(transaction):
    return merge(TRANSACTION_DEFAULTS, transaction)


UNSIGNED_TRANSACTION_FIELDS = (
    ('nonce', big_endian_int),
    ('systemContract', binary),
    ('gasPrice', big_endian_int),
    ('gasLimit', big_endian_int),
    ('to', Binary.fixed_length(20, allow_empty=True)),
    ('value', big_endian_int),
    ('data', binary),
    ('shardingFlag', big_endian_int),    # add for subchain
    ('via', Binary.fixed_length(20, allow_empty=True)),  # add for subchain
)


class Transaction(HashableRLP):
    fields = UNSIGNED_TRANSACTION_FIELDS + (
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
    )


class UnsignedTransaction(HashableRLP):
    fields = UNSIGNED_TRANSACTION_FIELDS


ChainAwareUnsignedTransaction = Transaction


def strip_signature(txn):
    unsigned_parts = itertools.islice(txn, len(UNSIGNED_TRANSACTION_FIELDS))
    return list(unsigned_parts)


def vrs_from(transaction):
    return (getattr(transaction, part) for part in 'vrs')
