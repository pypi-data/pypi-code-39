from base64 import b64decode, b64encode, urlsafe_b64decode
from enum import IntEnum
from os import urandom

import M2Crypto


class AESOperation(IntEnum):
    """ AES operation IDs """
    DECRYPT = 0
    ENCRYPT = 1


class AESCipher:
    """ Wrapper around M2Crypto to use AES cipher """

    ALGORITHM = 'aes_256_cbc'
    BLOCK_SIZE = 16

    def __init__(self, key: bytes):
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt given string using following scheme:
            {INITIALIZATION_VECTOR}{CIPHERTEXT}
        Where:
            * INITIALIZATION_VECTOR is with size of self.BLOCK_SIZE in bytes
            * CIPHERTEXT is our encrypted data
        """
        initialization_vector = self._generate_iv()
        cipher = self._get_cipher(initialization_vector, AESOperation.ENCRYPT)
        ciphertext = cipher.update(data) + cipher.final()
        return initialization_vector + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        """ Decrypt ciphertext containing IV, returning plaintext. """
        # Extract first {self.BLOCK_SIZE} bytes, containing our IV
        initialization_vector = data[:self.BLOCK_SIZE]
        # Extract ciphertext that is stored after IV
        ciphertext = data[self.BLOCK_SIZE:]
        # Ciphertext decryption using extracted IV
        cipher = self._get_cipher(initialization_vector, AESOperation.DECRYPT)
        return cipher.update(ciphertext) + cipher.final()

    def _get_cipher(self, initialization_vector, operation: AESOperation):
        return M2Crypto.EVP.Cipher(
            self.ALGORITHM, self.key, initialization_vector, operation
        )

    @classmethod
    def _generate_iv(cls) -> bytes:
        return urandom(cls.BLOCK_SIZE)


class AESCipherBase64(AESCipher):
    """ Use AESCipher with base64 encoded keys and inputs """

    def __init__(self, key: str):
        super().__init__(self.b64_decode_with_missing_padding(key))

    def encrypt(self, data: str) -> str:
        """ Encrypt string, returning ciphertext encoded in base64 """
        encrypted = super().encrypt(data.encode('utf-8'))
        return b64encode(encrypted).decode('utf-8')

    def decrypt(self, data: str) -> str:
        """ Returns decrypted plaintext """
        data = b64decode(data)
        return super().decrypt(data).decode('utf-8')

    @staticmethod
    def b64_decode_with_missing_padding(base64_text) -> bytes:
        """ Used for decoding key as its padding is stripped """
        base64_text += '=' * (len(base64_text) % 4)
        return urlsafe_b64decode(base64_text)
