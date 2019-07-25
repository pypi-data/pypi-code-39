from azure.keyvault import KeyVaultClient, KeyVaultAuthentication, KeyVaultId
import adal
import os
import traceback
import json
import tempfile
from .keyvault_tokenCache import TokenCache

def keyvault_client_auth():
    '''
    Fetch access-token to access key vault via device-code login on local side.
    Caches token credential for convenience afterwards.

    Returns
    -------
    obj
        Azure KeyVaultClient instance
    '''

    token_cache = TokenCache( tempfile.gettempdir() + '/token.json' )

    print('authenticates to the Azure Key Vault by providing a callback to authenticate using adal')

    # create an adal authentication context
    auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/301f59c4-c269-4a66-8a8c-f5daab211fa3')

    # using the XPlat command line client id as it is available across all tenants and subscriptions
    xplat_client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

    def adal_callback(server, resource, scope):
        if token_cache.valid():
            token = token_cache.load()

        # requires user login w/ device code
        else:
            user_code_info = auth_context.acquire_user_code(resource,
                                                        xplat_client_id)
            print(user_code_info['message'])
            token = auth_context.acquire_token_with_device_code(resource=resource,
                                                                client_id=xplat_client_id,
                                                                user_code_info=user_code_info)           
            token_cache.save( (token['tokenType'], token['accessToken']) )

        return token['tokenType'], token['accessToken']

    # create a KeyVaultAuthentication instance which will callback to the supplied adal_callback
    auth = KeyVaultAuthentication(adal_callback)

    # create the KeyVaultClient using the created KeyVaultAuthentication instance
    client = KeyVaultClient(auth)

    return client

def keyvault_getSecret(client):
    '''
    Fetches a secret on Azure Key Vault

    Parameters
    ----------
    client : obj
        Azure KeyVaultClient instance

    Returns
    -------
    int
        0 on success, -1 on error
    '''
       
    KEY_VAULT_URL = os.getenv('KEY_VAULT_URL')
    KEY_VAULT_SECRET_NAME = os.getenv('KEY_VAULT_SECRET_NAME')

    if not KEY_VAULT_URL or not KEY_VAULT_SECRET_NAME:
        print ('no valid key vault information given')
        return -1

    print('getting secret...')
    try:
        secret_bundle = client.get_secret(KEY_VAULT_URL, 
                                          KEY_VAULT_SECRET_NAME, 
                                          secret_version=KeyVaultId.version_none)
        print( secret_bundle )
        return 0
    except:
        return -1

def keyvault_importCertificate(client, certfile):
    '''
    Upload a certificate to Azure Key Vault

    Parameters
    ----------
    client : obj
        Azure KeyVaultClient instance
    certfile : str (bytes?)
        base64 encoded certificate with private key attached

    Returns
    -------
    int
        0 on success, -1 on error
    '''

    KEY_VAULT_URL = os.getenv('KEY_VAULT_URL')
    KEY_VAULT_CERT_NAME = os.getenv('KEY_VAULT_CERT_NAME')
    
    if not KEY_VAULT_URL or not KEY_VAULT_CERT_NAME:
        print ('no valid key vault information given')
        return -1

    try:
        print('uploading certificate to key vault...')
        cert_op = client.create_certificate(KEY_VAULT_URL, KEY_VAULT_CERT_NAME, certfile)
        print(cert_op)
        return 0
    except:
        return -1