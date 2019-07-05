import json
import struct

PREFIX_FMT = '!l'
PREFIX_SIZE = 4

# header: dict
# payload: bytes
def make_request(header, payload=None):
  buffer = bytearray(PREFIX_SIZE)
  header = bytes(json.dumps(header), 'utf-8')
  struct.pack_into(PREFIX_FMT, buffer, 0, len(header))
  buffer.extend(header)
  if payload: buffer.extend(payload)
  # print("Encoded message: header: {} bytes, payload: {} bytes".format(len(header), len(payload)))
  return bytes(buffer)

def parse_request(data):
  header_len, *_ = struct.unpack_from(PREFIX_FMT, data, 0)
  header_bytes = data[PREFIX_SIZE : header_len + PREFIX_SIZE]
  header = json.loads(header_bytes.decode('utf-8'))
  payload = data[header_len + PREFIX_SIZE:]
  # print("Decoded message: header: {} bytes, payload: {} bytes".format(len(header_bytes), len(payload)))
  return header, payload