import base64
import json
import os
import shutil
import tempfile
import time
from unittest import TestCase

from nacl.exceptions import BadSignatureError
from nacl.public import Box, PrivateKey, PublicKey, SealedBox

from . import library

class Base64(TestCase):
    def test_b64(self):
        self.assertEqual(library.b64(b'foo'), 'Zm9v')
        self.assertRaises(TypeError, library.b64, 'foo')

    def test_b64_key(self, seed='0'*32):
        sk = PrivateKey(seed.encode('utf-8'))
        self.assertEqual(library.b64_key(sk), 'MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA=')

    def test_unb64(self):
        self.assertEqual(library.unb64('Zm9v'), b'foo')

class MakingKeys(TestCase):
    def test_from_byte_string(self, seed=b'1'*32):
        bytestring = base64.urlsafe_b64encode(seed)
        key = library.public_key(bytestring)
        self.assertEqual(key, PublicKey(b'1'*32))

class JointEncryption(TestCase):
    def setUp(self):
        self.sk1, self.pk1 = library.new_encryption_keypair()
        self.sk2, self.pk2 = library.new_encryption_keypair()
        self.signing1, self.verify1 = library.new_signature_keypair()
        self.signing2, self.verify2 = library.new_signature_keypair()

    def test_jointly_encrypt(self):
        data = {'foo': 'bar', 'baz': 'frob'}
        blob = library.jointly_encrypt(self.sk1, self.pk2, data)
        box = Box(self.sk2, self.pk1) # swap the keys around to decrypt
        envelope = library.unb64(blob)
        text = box.decrypt(envelope).decode('utf-8')
        self.assertEqual(json.loads(text), data)

    def test_jointly_decrypt(self):
        plaintext = {'foo': 'bip', 'bar': 'bork'}
        crypttext = library.jointly_encrypt(self.sk1, self.pk2, plaintext)

        # verify we can handle non-b64 input
        decrypted = library.jointly_decrypt(self.sk1, self.pk1, '')
        self.assertIsNone(decrypted)

        # verify using the wrong keys returns None
        decrypted = library.jointly_decrypt(self.sk1, self.pk1, crypttext)
        self.assertIsNone(decrypted)

        # now do it with the right keys (note they're swapped from the encrypt call)
        decrypted = library.jointly_decrypt(self.sk2, self.pk1, crypttext)
        self.assertEqual(decrypted, plaintext)

    def test_seal_and_sign(self):
        plaintext = {'kris': 'kringle', 'fish': 'sticks'}
        signcrypt = library.seal_and_sign(self.signing1, self.pk2, plaintext)
        self.assertIsNotNone(signcrypt)

        unwrapped = library.unb64(signcrypt)
        verified  = self.verify1.verify(unwrapped)
        self.assertIsNotNone(verified)

        with self.assertRaises(BadSignatureError):
            self.verify2.verify(unwrapped)

        sealedbox = SealedBox(self.sk2)
        recovered = sealedbox.decrypt(verified).decode('utf-8')
        self.assertEqual(json.loads(recovered), plaintext)


class Configuration(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_saving_config(self):
        path = os.path.join(self.tmpdir, '.watchdog/key')
        library.save_config(path, FOO='BAR', BAZ_BAZ='frobble', BYTE=b'BIT')
        self.assertTrue(os.path.exists(path))
        with open(path, 'r') as f:
            contents = [line.strip() for line in f]
        self.assertIn("FOO = 'BAR'", contents)
        self.assertIn("BAZ_BAZ = 'frobble'", contents)
        self.assertIn("BYTE = b'BIT'", contents)

    def tearDown(self):
        abspath = os.path.abspath(self.tmpdir)
        shutil.rmtree(abspath)

class FilePatterns(TestCase):
    nginx_lines = [
        '51.254.59.113 - - [14/Jul/2019:14:44:20 +0000] "GET / HTTP/1.1" 444 0 "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"',
        '43.82.6.1 - - [1/Jun/2029:04:16:21 +0000] "GET /watchdog/delay-under-3600/%d  HTTP/1.1" 400 0 "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"' % int(time.time()),
        '43.82.6.1 - - [1/Jun/2029:04:16:21 +0000] "GET /watchdog/delay-over-3600/%d  HTTP/1.1" 400 0 "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"' % (int(time.time()) - 3601,),
    ]

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.nginx_file = os.path.join(self.tmpdir, 'nginx.log')
        with open(self.nginx_file, 'w') as f:
            f.write('\n'.join(FilePatterns.nginx_lines) + '\n')

    def test_missing_file(self):
        self.assertIsNone(library.parse_file('nothing-is-here'))

    def test_unreadable_file(self):
        filename = os.path.join(self.tmpdir, 'will-be-unreadable')
        with open(filename, 'w') as f:
            f.write('')
        self.assertEqual(library.parse_file(filename), [])
        os.chmod(filename, 0o333)
        self.assertIsNone(library.parse_file(filename))

    def test_nginx(self):
        messages = library.parse_file(self.nginx_file, max_delay=3600)
        self.assertIn('delay-under-3600', messages)
        self.assertNotIn('delay-over-3000', messages)

    def tearDown(self):
        abspath = os.path.abspath(self.tmpdir)
        shutil.rmtree(abspath)

class Commandments(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_run_normally(self):
        result = library.run(['uname'])
        self.assertEqual(result['stdout'], 'Linux\n')

    def test_output_from_stdout_and_stderr(self):
        result = library.run("grep Watchdog README.md file-doesnt-exist".split())
        self.assertEqual(result['stdout'], 'README.md:Watchdog\n')
        self.assertIn('No such file or directory', result['stderr'])

    def test_non_utf8_output(self):
        # Get a bunch of bytes which will definitely have some non-UTF8 members
        result = library.run("head -c 256 /dev/urandom".split())
        self.assertTrue(len(result['stdout']) > 0)

    def test_bad_command_input(self):
        result = library.run("foo bar")
        self.assertEqual(result['command'], 'foo bar')
        self.assertIn('FileNotFoundError', result['stderr'])

    def test_append_to_file(self):
        filename = os.path.join(self.tmpdir, 'fromble')
        with open(filename, 'w') as f:
            f.write('monday')
        cmd = ['python', '-c', r"open('%s', 'a').write('foo bar baz\n')" % filename]
        result = library.run(cmd)
        with open(filename, 'r') as f:
            contents = f.read()
        self.assertIn('foo bar baz', contents)
        self.assertIn('monday', contents)

    def tearDown(self):
        abspath = os.path.abspath(self.tmpdir)
        shutil.rmtree(abspath)
