# coding:utf-8

import logging
import os
from core.exception import error_msg
from core.exception import error_code
from core.exception import exceptions
from core.auth import credentials
from core.auth.signers import access_key_signer
from core.auth.signers import rsa_key_pair_signer


class SignerFactory(object):
    @staticmethod
    def get_signer(cred, region_id, do_action_api, debug=False):
        if cred.get('ak') is not None and cred.get('secret') is not None:
            access_key_credential = credentials.AccessKeyCredential(
                cred.get('ak'), cred.get('secret'))
            return access_key_signer.AccessKeySigner(access_key_credential)
        elif os.environ.get('ACCESS_KEY_ID') is not None \
                and os.environ.get('ACCESS_KEY_SECRET') is not None:
            access_key_credential = credentials.AccessKeyCredential(
                os.environ.get('ACCESS_KEY_ID'),
                os.environ.get('ACCESS_KEY_SECRET'))
            return access_key_signer.AccessKeySigner(access_key_credential)
        elif cred.get('credential') is not None:
            credential = cred.get('credential')
            if isinstance(credential, credentials.AccessKeyCredential):
                return access_key_signer.AccessKeySigner(credential)
            elif isinstance(credential, credentials.RsaKeyPairCredential):
                return rsa_key_pair_signer.RsaKeyPairSigner(credential, region_id, debug)
        elif cred.get('public_key_id') is not None and cred.get('private_key') is not None:
            logging.info(
                "'ClickClient(regionId, pub_key_id, pri_key)' is deprecated")
            rsa_key_pair_credential = credentials.RsaKeyPairCredential(cred['public_key_id'],
                                                                       cred['private_key'],
                                                                       cred['session_period'])
            return rsa_key_pair_signer.RsaKeyPairSigner(rsa_key_pair_credential, region_id, debug)
        else:
            raise exceptions.ClientException(error_code.SDK_INVALID_CREDENTIAL,
                                             error_msg.get_msg('SDK_INVALID_CREDENTIAL'))
