from .utils import to_bytes

from typing import List

_name_char = '.12345abcdefghijklmnopqrstuvwxyz'


def _serialize_var_uint32(n: int)->bytes:
    r = bytearray()

    while True:
        if n >> 7:
            r.append(0x80 | (n & 0x7f))
            n >>= 7
        else:
            r.append(n)
            break

    return bytes(r)


def _serialize_name(s: str)->bytes:
    s_int = 0
    for c in s:
        s_int = (s_int << 5) + _name_char.index(c)
    s_int <<= 64 - len(s) * 5

    return to_bytes(s_int, size=8, byteorder='little')


def _serialize_permission(actor: str, permission: str)->bytes:
    return b''.join((
        _serialize_name(actor),
        _serialize_name(permission),
    ))


def _serialize_action(account: str, name: str, authorization: List[dict], hex_data: bytes)->bytes:
    return b''.join((
        _serialize_name(account),
        _serialize_name(name),
        _serialize_var_uint32(len(authorization)),
    ) + tuple(_serialize_permission(permission['actor'], permission['permission']) for permission in authorization) + (
        _serialize_var_uint32(len(hex_data)),
        hex_data,
    ))


def serialize_transaction(expiration: int,
                          ref_block_num_bytes: bytes, ref_block_prefix: bytes,
                          actions: List[dict])->bytes:
    return b''.join((
        to_bytes(expiration, 4, 'little'),  # expiration
        ref_block_num_bytes,  # ref_block_num
        ref_block_prefix,  # ref_block_prefix
        b'\x00'  # max_net_usage_words
        b'\x00'  # max_cpu_usage_ms
        b'\x00'  # delay_sec
        b'\x00',  # context_free_actions
        _serialize_var_uint32(len(actions)),
    ) + tuple(_serialize_action(action['account'], action['name'], action['authorization'], bytes.fromhex(action['data'])) for action in actions) + (
        b'\x00',  # transaction_extensions
    ))
