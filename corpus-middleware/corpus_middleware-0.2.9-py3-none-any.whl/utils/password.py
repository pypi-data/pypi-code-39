from base64 import b64encode, b64decode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

encoding = "UTF-8"

PK = ("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCX4kRYjU6XclWT4mwxgQ55JerRar8"
      "CPEHp4uZRITqZuk8p0z5UTL02muequw2dgvgNlJkE8C7eyXf1S8TH+MvbVkHnCoKKig"
      "APb08PtqcvVIqnZn+kNDpiQZapkpHrEXeR+rWfj3etTwMHYbV+zTaKOdxa7fm3oO4CW"
      "bgmfkSC8wIDAQAB")


class PassWord:

    @classmethod
    def rsa_encrypt(cls, plain_text, public_key=PK):
        key = RSA.importKey(b64decode(public_key))
        cipher = PKCS1_v1_5.new(key)
        cipher_text = cipher.encrypt(plain_text.encode(encoding))
        return b64encode(cipher_text)
