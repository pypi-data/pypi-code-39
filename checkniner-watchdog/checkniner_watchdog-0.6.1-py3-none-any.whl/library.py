import base64
import json
import logging
import os
import re
import subprocess
import sys
import time

from nacl.exceptions import CryptoError
from nacl.public import Box, PrivateKey, PublicKey, SealedBox
from nacl.signing import SigningKey
import requests

log = logging.getLogger('watchdog.watchdog')

nginx = re.compile('(?P<prefix>.*) "GET /watchdog/(?P<message>[-_A-Za-z0-9=]+)/(?P<timestamp>[0-9]{1,11}) (?P<suffix>.*)')

def b64(bytestring):
    return base64.urlsafe_b64encode(bytestring).decode('utf-8')

def unb64(string):
    return base64.urlsafe_b64decode(string)

def b64_key(nacl_key):
    return b64(nacl_key.encode())

def new_encryption_keypair():
    sk = PrivateKey.generate()
    return (sk, sk.public_key)

def new_signature_keypair():
    sk = SigningKey.generate()
    return (sk, sk.verify_key)

def public_key(bytestring):
    return PublicKey(unb64(bytestring))

def private_key(bytestring):
    return PrivateKey(unb64(bytestring))

def signing_key(bytestring):
    return SigningKey(unb64(bytestring))

def save_config(path, **kwargs):
    try:
        os.mkdir(os.path.dirname(path))
    except FileExistsError:
        pass
    with open(path, 'w') as f:
        for key, value in kwargs.items():
            f.write('%s = %r\n' % (key, value))

def jointly_encrypt(our_sk, their_pk, data):
    bytestring = json.dumps(data).encode('utf-8')
    encrypted = Box(our_sk, their_pk).encrypt(bytestring)
    return b64(encrypted)

def jointly_decrypt(our_sk, their_pk, data):
    try:
        encrypted = unb64(data)
    except:
        log.debug("Unable to b64_decode '%s'" % data)
        return None
    try:
        payload = Box(our_sk, their_pk).decrypt(encrypted)
    except CryptoError:
        log.debug("Unable to decrypt '%s' with these keys. Corrupt message? Wrong keys?" % data)
        return None
    return json.loads(payload.decode('utf-8'))

def seal_and_sign(our_signkey, their_publickey, data):
    bytestring = json.dumps(data).encode('utf-8')
    encrypted = SealedBox(their_publickey).encrypt(bytestring)
    signed = our_signkey.sign(encrypted)
    return b64(signed)

def witness(server, publickey, documents):
    url = '%s/witnesses/%s' % (server, b64_key(publickey))
    log.debug("Posting to URL: %s" % url)
    r = requests.post(url, data={'data': documents})
    log.debug("Witness server responded with status=%d" % r.status_code)

def witness_statement(server, publickey, details):
    url = '%s/witnesses/%s/statements' % (server, b64_key(publickey))
    log.debug("Posting to URL: %s" % url)
    r = requests.post(url, data={'data': details})
    log.debug("Witness server responded with status=%d" % r.status_code)

def parse_file(filepath, pattern=nginx, max_delay=3600):
    messages = None
    try:
        f = open(filepath, 'r')
    except FileNotFoundError:
        log.error("File '%s' does not exist" % filepath)
    except PermissionError:
        log.error("File '%s' exists but no read permissions granted" % filepath)
    except Exception as exc:
        log.exception("Unable to read file '%s', though it seems to exist" % filepath)
    else:
        messages = []
        for line in f:
            m = pattern.match(line.strip())
            if m:
                delay = int(time.time()) - int(m.group('timestamp'))
                if delay > max_delay:
                    log.debug("Rejecting message with delay of %d" % delay)
                    continue
                messages.append(m.group('message'))
    finally:
        try:
            f.close()
        except UnboundLocalError:
            pass
    return messages

def run(command):
    log.debug("Running: %s" % command)
    started = time.time()
    try:
        runner = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as exc:
        runner = False
        error = exc
    return {
        'command': command,
        'elapsed': round(time.time() - started, 1),
        'started': round(started, 3),
        'status':  runner.returncode if runner else 'None',
        'stdout':  runner.stdout.decode('utf-8', 'replace') if runner else 'None',
        'stderr':  runner.stderr.decode('utf-8', 'replace') if runner else '%r' % error,
    }
