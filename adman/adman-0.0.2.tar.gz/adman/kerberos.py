# https://wiki.samba.org/index.php/Configure_DHCP_to_update_DNS_records_with_BIND9
from subprocess import check_call, call
import logging
import os

logger = logging.getLogger(__name__)

def request_new_tgt(principal, keytab, cache):
    args = [
        'kinit',

        # request non-forwardable tickets
        '-F',

        # request a ticket using a key in this local keytab file
        '-k', '-t', str(keytab),

        # store tickets in this cache
        '-c', str(cache),

        principal,
    ]
    logger.debug("Running `{}`".format(' '.join(args)))
    check_call(args)


def check_cred_cache(cache):
    args = [
        'klist',
        '-c', str(cache),
        # silent -- exit with 1 if unreadable or expired
        '-s',
    ]
    logger.debug("Running `{}`".format(' '.join(args)))
    rc = call(args)
    return rc == 0


def ensure_valid_tgt(**kw):
    if not check_cred_cache(kw['cache']):
        logger.info("Cache expired; requesting new ticket")
        request_new_tgt(**kw)


def make_principal(primary, realm, instance=None):
    result = primary
    if instance:
        result += '/' + instance
    result += '@' + realm.upper()
    return result


def setup_kerberos_environ(username, domain, keytab, cache):
    principal = make_principal(username, domain)
    logger.info("Using kerberos principal {}".format(principal))

    ensure_valid_tgt(
            principal = principal,
            keytab = keytab,
            cache = cache,
        )
    os.environ['KRB5CCNAME'] = str(cache)


if __name__ == '__main__':
    def parse_args():
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument('principal')
        ap.add_argument('-k', dest='keytab', required=True)
        ap.add_argument('-c', dest='cache', required=True)
        return ap.parse_args()

    def main():
        logging.basicConfig(level=logging.DEBUG)

        args = parse_args()

        ensure_valid_tgt(
                principal = args.principal, 
                keytab = args.keytab,
                cache = args.cache,
            )

    main()
