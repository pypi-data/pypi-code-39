from cryptography.fernet import Fernet
import binascii


class Notary:
    cryptographer = None

    def __init__(self, key):
        if type(key) != bytes:
            key = self.to_bytes(key)
        try:
            self.cryptographer = Fernet(key)
        except binascii.Error:
            raise ValueError("Key is not valid")

    def decrypt(self, data_to_decrypt):
        if type(data_to_decrypt) != bytes:
            data_to_decrypt = self.to_bytes(data_to_decrypt)
        try:
            return self.cryptographer.decrypt(data_to_decrypt)
        except binascii.Error:
            return False

    @staticmethod
    def to_bytes(input_data):
        return bytes(input_data, encoding='utf-8')
