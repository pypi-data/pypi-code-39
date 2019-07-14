from missinglink.crypto import Cipher


class GcpKms(Cipher):

    def __init__(self, key_path):
        self.key_path = key_path

    @staticmethod
    def get_kms_client():
        try:
            from google.cloud import kms_v1
        except ImportError:
            raise ImportError('google-cloud-kms not found. It must be installed for this cipher')

        return kms_v1.KeyManagementServiceClient()

    def encrypt(self, data):
        client = self.get_kms_client()

        response = client.encrypt(self.key_path, data)
        return response.ciphertext

    def decrypt(self, data):
        client = self.get_kms_client()

        response = client.decrypt(self.key_path, data)
        return response.plaintext
