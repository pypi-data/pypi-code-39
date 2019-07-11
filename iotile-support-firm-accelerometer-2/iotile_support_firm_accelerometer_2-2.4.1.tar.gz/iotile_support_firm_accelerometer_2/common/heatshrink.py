"""Simple implementation of the Heatshrink compression library."""

from builtins import range
from iotile.core.exceptions import ExternalError

try:
    from bitstring import BitArray, ConstBitStream
except ImportError:
    raise ExternalError("You must have the bitstring package installed from pip to use this", suggestion="pip install bitstring")


class Heatshrink(object):
    """Pure python implementation of heatshrink."""

    def __init__(self, window_bits=8, lookahead_bits=4):
        self.window_bits = window_bits
        self.lookahead_bits = lookahead_bits

        self.window = bytearray(2 ** self.window_bits)
        self.window_head = 0
        self.output = bytearray([])

    def encode(self, byte_data):
        """Encode a series of bytes into a heatshrink encoded bitstream.

        This does not actually compress anything, it just emits each byte as a
        literal value but it produces a valid heatshrink bitstream and doesn't
        require complex back-reference calculations.  So the output is
        actually 9/8 larger than the input.

        Returns:
            bytes: The encoded data (also as bytes).
        """

        output = BitArray()
        one_bit = BitArray(bin='0b1')

        assert len(one_bit) == 1

        for byte in bytearray(byte_data):
            output.append(one_bit)
            output.append(BitArray(length=8, uint=byte))

        assert len(output) == 9*(len(byte_data))

        remaining = len(output) % 8
        if remaining != 0:
            output += BitArray(length=(8 - remaining))

        return output.bytes

    def decode(self, data):
        """Decode heatshrink compressed data."""

        input_buffer = ConstBitStream(data)

        while len(input_buffer) - input_buffer.pos >= 8:
            is_literal = input_buffer.read("bool")
            if is_literal:
                val = input_buffer.read('uint:8')
                self._emit_byte(val)
            elif (len(input_buffer) - input_buffer.pos) >= (self.window_bits + self.lookahead_bits):
                index = input_buffer.read("uintbe:%d" % self.window_bits)
                count = input_buffer.read("uint:%d" % self.lookahead_bits)

                index += 1
                count += 1

                for _i in range(0, count):
                    neg_index = self.window_head - index

                    val = self.window[neg_index]
                    self._emit_byte(val)
            else:
                break

        return self.output

    def _emit_byte(self, value):
        self.output.append(value)
        self.window[self.window_head] = value
        self.window_head += 1

        if self.window_head == len(self.window):
            self.window_head = 0
