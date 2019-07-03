from django.test import TestCase

from .crypto import AESCipher, AESCipherBase64


class AESCipherTestCase(TestCase):

    BINARY_ENCRYPTION_KEY = b'TEST_BINARY_ENCRYPTION_KEY'
    ENCRYPTION_KEY = 'F5o77VF5ZbsLlUJncgMAtU_cf56WBIORSOyp4-x5wbc===='

    PLAINTEXT = 'To be encrypted 1234.'
    BINARY_DATA = b'TEST_BINARY_DATA'

    def test_aes_cipher_binary_data_encryption_decryption(self):
        cipher = AESCipher(self.BINARY_ENCRYPTION_KEY)
        encrypted = cipher.encrypt(self.BINARY_DATA)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(decrypted, self.BINARY_DATA)
        self.assertNotEqual(encrypted, self.BINARY_DATA)

    def test_base64_string_encryption_decryption_flow(self):
        cipher = AESCipherBase64(self.ENCRYPTION_KEY)
        encrypted = cipher.encrypt(self.PLAINTEXT)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(decrypted, self.PLAINTEXT)
        self.assertNotEqual(encrypted, self.PLAINTEXT)
