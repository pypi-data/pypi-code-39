import os


class Config(object):
    """The Config object holds configuration information.

    Args:
        None

    Attributes:
        DEBUG (bool): Debug mode
        LOG_LEVEL (str): Logger Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        IPA_HOST (str): FreeIPA server hostname
        PRINCIPAL (str): FreeIPA user
        PASSWORD (str): FreeIPA user password
        AWS_REGION (str): AWS Region
    """
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    IPA_HOST = os.environ.get('IPA_HOST') or 'locahost'
    PRINCIPAL = os.environ.get('PRINCIPAL') or 'admin'
    PASSWORD = os.environ.get('PASSWORD') or \
        'this-really-needs-to-be-changed'
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-east-1'


config = Config()
