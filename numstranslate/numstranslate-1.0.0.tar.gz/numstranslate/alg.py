def dec_to_bin(decimal_number, bit_depth=0):
    """
    Accepts a decimal integer.
    Returns a binary number in a string.
    Optional parameter takes the bit depth: up to how many bits need to add the number
    """
    if decimal_number == 0:
        return '0' if bit_depth == 0 else '0' * bit_depth

    binary_number = ''

    while decimal_number > 0:
        bit = decimal_number % 2
        binary_number = str(bit) + binary_number
        decimal_number = (decimal_number - bit) // 2

    if bit_depth != 0:
        amount_bits_fill = bit_depth - len(binary_number)
        bits_fill = '0' * amount_bits_fill
        return bits_fill + binary_number
    return binary_number


def bin_to_dec(binary_number):
    """
    Accepts an integer binary number in a string.
    Returns a decimal number.
    """
    bits_list = []
    for bit in binary_number:
        bits_list.append(int(bit))

    decimal_number = 0
    for bit_position, bit in enumerate(reversed(bits_list)):
        decimal_number += bit * 2 ** bit_position
    return decimal_number


def dec_to_hex(decimal_number):
    """
    Accepts a decimal integer.
    Returns a hexadecimal number in a string.
    """
    hex_char = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    hex_number = ''

    while decimal_number > 0:
        hex = decimal_number % 16
        decimal_number = (decimal_number - hex) // 16
        if hex >= 10:
            hex_number = hex_char[hex] + hex_number
            continue
        hex_number = str(hex) + hex_number

    return hex_number


def hex_to_dec(hex_number):
    """
    Accepts an integer hexadecimal number in a string.
    Returns a decimal number.
    """
    hex_char = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    hex_list = []
    for hex in hex_number:
        if hex in hex_char:
            hex_list.append(hex_char[hex])
            continue
        hex_list.append(int(hex))

    decimal_number = 0
    for hex_position, hex in enumerate(reversed(hex_list)):
        decimal_number += hex * 16 ** hex_position
    return decimal_number
