import logging
import os
import sys

import click

from . import library

logging.basicConfig(**{
    'datefmt':  '%Y-%m-%d %H:%M:%S',
    'stream': sys.stdout,
    'format':   '%(asctime)s |%(levelname).1s| %(message)s',
    'level':    'INFO',
})
log = logging.getLogger(__name__)

WATCHDOG_PK_RAW = b'APDHzZHs8mmlXle5XPlzRMWOO1-3pHSINmLO2Uw9IFA='
CONFIG_PATH = None

@click.group(options_metavar='[COMMON OPTIONS]')
@click.version_option(message='%(prog)s version %(version)s')
@click.option('--config', default='/root/.watchdog', help='Where config details should be kept', show_default=True, metavar='<dir>')
@click.option('--verbose', is_flag=True, help='Log extra details about operations')
def watchdog(config, verbose):
    """Watchdog: The ever-vigilant security assistant.

    For help with a command: watchdog COMMAND --help
    """
    if verbose:
        log.setLevel('DEBUG')
    global CONFIG_PATH
    CONFIG_PATH = config


@watchdog.command()
@click.option('--extra', multiple=True, help='Additional details to witness', metavar='<key=value>')
@click.option('--witness', default='https://checkniner-witness.herokuapp.com', help='The Witness server for enrolling and testifying', show_default=True, metavar='<server>')
@click.option('--reset', is_flag=True, help='Overwrite existing configuration')
def init(witness, extra, reset):
    """Generate keys and prepare environment"""
    log.debug("Initializing with witness server %s and config dir '%s'" % (witness, CONFIG_PATH))

    config = os.path.join(CONFIG_PATH, 'keys')
    if os.path.exists(config) and len(open(config, 'r').read()) > 0:
        if not reset:
            log.error("The config dir '%s' has already been initialized, nothing to do" % CONFIG_PATH)
            log.error("(if you'd like to re-initialize, use the '--reset' flag)")
            sys.exit(0)
        else:
            log.info("Removing existing config and re-initalizing")
            os.unlink(config)

    log.debug("Using watchdog publickey '%s'" % WATCHDOG_PK_RAW.decode('utf-8'))
    watchdog_pk = library.public_key(WATCHDOG_PK_RAW)

    log.debug("Generating local keypairs")
    encrypt_sk, encrypt_pk = library.new_encryption_keypair()
    signing_sk, signing_pk = library.new_signature_keypair()

    log.debug("Saving config & keys to '%s'" % config)
    library.save_config(
        config,
        WITNESS_URL=witness,
        WATCHDOG_PK_RAW=WATCHDOG_PK_RAW,
        ENCRYPT_KEY_RAW=library.b64_key(encrypt_sk).encode('utf-8'),
        SIGNING_KEY_RAW=library.b64_key(signing_sk).encode('utf-8')
    )

    documents = {k:v for k,v in [ex.split('=') for ex in extra if '=' in ex]}
    # Do these after the extras so that they can't get overwritten
    documents.update({
        'publickey': library.b64_key(encrypt_pk),
        'verifykey': library.b64_key(signing_pk),
    })
    log.debug('Collected witness documents: %r' % documents)
    documents = library.jointly_encrypt(encrypt_sk, watchdog_pk, documents)
    library.witness(witness, encrypt_pk, documents)
    log.debug("Initialization and enrollment completed")


@watchdog.command()
@click.option('-t', '--keytype', type=click.Choice(['encrypting', 'signing']), default='encrypting', show_default=True, help='The type of key pair to generate')
def keygen(keytype):
    """Generate a one-off pair of keys"""
    if keytype == 'encrypting':
        sk, pk = library.new_encryption_keypair()
        s_type, p_type = ('Private', 'Public')
    else:
        sk, pk = library.new_signature_keypair()
        s_type, p_type = ('Signing', 'Verify')
    print("%s key: %s" % (s_type, library.b64_key(sk)))
    print("%s key: %s" % (p_type, library.b64_key(pk)))


@watchdog.command()
@click.option('--file', 'filepath', default='/var/log/nginx/access.log', help='The file to review', show_default=True, metavar='<path>')
@click.option('--max-delay', default=3600, help='The number of seconds which can elapse before an action is expired', show_default=True, metavar='<seconds>')
def patrol(filepath, max_delay, config_file='keys'):
    """Check the environment for suspicious activity"""
    log.info("Patrolling file '%s'" % filepath)
    log.debug("Loading configuration from config dir %s" % CONFIG_PATH)
    config = os.path.join(CONFIG_PATH, 'keys')
    try:
        with open(config, 'r') as f:
            for line in f:
                exec(line.strip(), globals())
    except PermissionError:
        log.error("Can't read configuration details from '%s'" % config)
        sys.exit(1)

    log.debug("Using watchdog publickey '%s'" % WATCHDOG_PK_RAW.decode('utf-8'))
    watchdog_pk = library.public_key(WATCHDOG_PK_RAW)
    encrypt_sk = library.private_key(ENCRYPT_KEY_RAW)
    log.debug("Our publickey is '%s'" % library.b64_key(encrypt_sk.public_key))
    signing_sk = library.signing_key(SIGNING_KEY_RAW)

    messages = library.parse_file(filepath, max_delay=max_delay)
    if messages is None:
        log.error("Unable to finish the patrol. Something is very wrong.")
        sys.exit(1)
    for message in messages:
        log.debug("Found message: '%s'" % message)
        verified = library.jointly_decrypt(encrypt_sk, watchdog_pk, message)
        if verified is None:
            log.warn("Ignoring unauthorized message '%s'" % message)
            continue

        if 'command' not in verified:
            log.info("No command included in verified message, nothing to do")
            continue
        results = library.run(verified['command'])

        details = {
            'results': results,
            'instructions': verified,
        }
        log.debug("Collected details for statement: %r" % details)
        details = library.seal_and_sign(signing_sk, watchdog_pk, details)
        library.witness_statement(WITNESS_URL, encrypt_sk.public_key, details)
        log.info("Witness statement recorded")

    log.info("Patrol completed")


@watchdog.command()
def wipe():
    """Remove everything related to this tool"""
    log.info("Not Implemented Yet: Wiping")
    log.debug("Not Implemented Yet: Removing configuration files")
    log.debug("Not Implemented Yet: Removing log files")
    log.debug("Not Implemented Yet: Removing executables and scripts")


if __name__ == '__main__':
    watchdog()
