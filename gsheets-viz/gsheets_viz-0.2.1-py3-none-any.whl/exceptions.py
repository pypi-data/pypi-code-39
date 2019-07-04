from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class InvalidCredential(Exception):
    pass


class InvalidSupportType(Exception):
    pass


class InvalidRequiredValue(Exception):
    pass


class CredentialFormatException(Exception):
    pass


class EncodeUrlException(Exception):
    pass


class ExchangeCredentialException(Exception):
    pass


class ParseResponseException(Exception):
    pass


class VisualizeResponseException(Exception):
    pass
