import base64
import hashlib

from Crypto.Cipher import DES3


class Capicom3DESCipher():

    # this is full of much magic. Credit where credit is due:
    # https://social.msdn.microsoft.com/Forums/en-US/45a93a86-52d5-4067-9bc8-9303acf2eb49/how-to-decrypt-capicom-des-encrypted-data-in-net?forum=Vsexpressvb
    # https://web.archive.org/web/20170424032731/http://www.jensign.com/JavaScience/dotnet/DeriveBytes/
    # https://lapo.it/asn1js/#MGIGCSsGAQQBgjdYA6BVMFMGCisGAQQBgjdYAwGgRTBDAgMCAAECAmYDAgIAwAQIH20CzGB8o_gEECFOPw_ORkGak4_TJOS8HpcEGFlehZB8Snsu7cNBderja7W2eRUOKK53QA
    # https://microsoft.public.platformsdk.security.narkive.com/cY1ITD6t/urgent-trouble-with-capicom-and-triple-des-encryption-decryption#post2
    # https://docs.microsoft.com/en-us/windows/desktop/api/Wincrypt/nf-wincrypt-cryptderivekey

    # some of the code is based on (or direct quotes from) wincrypto, which is MIT licensed by crappycrypto
    # https://github.com/crappycrypto/wincrypto

    # the string from realpage is a base64 encoded asn.1 stream
    # the locations of the iv, salt, and cipher text in the binary are consistent, so we can just reference their locations with magic numbers
    # the encrypted content is encrypted with triple des encryption
    # the encryption key is generated as such:
    #   sha1 hash the utf-16le bytes of the password and bytes of the salt together
    #   then the algorithm detailed at https://docs.microsoft.com/en-us/windows/desktop/api/Wincrypt/nf-wincrypt-cryptderivekey
    #   truncate the result to the first 24 bytes
    # the original data was padded using PKCS5, so we can just strip out the padding characters at the end
    @classmethod
    def decrypt_3des_realpage(cls, encrypted, password):
        encrypted_bytes = base64.b64decode(encrypted)
        initialization_vector, salt, cipher_text = cls.extract_relevant_fields(encrypted_bytes)
        key = cls._triple_des_derive_key(password, salt)
        ssn_decrypted = DES3.new(key, DES3.MODE_CBC, initialization_vector).decrypt(cipher_text)

        # https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS%235_and_PKCS%237
        # this strips off the PKCS5 padding by using the last character (representing the number of bytes to remove)
        # windows uses utf-16le unicode for the text encoding
        return (ssn_decrypted[0:-ssn_decrypted[-1]]).decode('utf-16le')

    @classmethod
    def extract_relevant_fields(cls, encrypted_bytes):
        initialization_vector = encrypted_bytes[48:48 + 8]
        salt = encrypted_bytes[58:58 + 16]
        cipher_text = encrypted_bytes[76:]
        return initialization_vector, salt, cipher_text

    @classmethod
    def _triple_des_derive_key(cls, password, salt):
        hash_val = cls._sha1_hash(password.encode('utf-16le') + salt)
        buf1 = bytearray(b'\x36' * 64)
        for x in range(len(hash_val)):
            buf1[x] ^= hash_val[x]
        buf2 = bytearray(b'\x5c' * 64)
        for x in range(len(hash_val)):
            buf2[x] ^= hash_val[x]
        derived_key = cls._sha1_hash(buf1) + cls._sha1_hash(buf2)
        return derived_key[:24]

    @classmethod
    def _sha1_hash(cls, data):
        hasher = hashlib.sha1()
        hasher.update(data)
        return hasher.digest()
