from gsheetsviz.connector import init as connector
from gsheetsviz.exceptions import (
    InvalidCredential,
    InvalidSupportType,
    InvalidRequiredValue,
    CredentialFormatException,
    EncodeUrlException,
    ExchangeCredentialException,
    ParseResponseException,
    VisualizeResponseException,
)

__all__ = [
    'connector',
    'apilevel',
    'threadsafety',
    'paramstyle',
    'InvalidCredential',
    'InvalidSupportType',
    'InvalidRequiredValue',
    'CredentialFormatException',
    'EncodeUrlException',
    'ExchangeCredentialException',
    'ParseResponseException',
    'VisualizeResponseException',
]

apilevel = '2.0'
# Threads may share the module and connections
threadsafety = 2
paramstyle = 'pyformat'
