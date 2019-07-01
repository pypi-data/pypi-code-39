import os


class Config(object):
    DEBUG = False
    TESTING = False
    IPA_HOST = os.environ.get('IPA_HOST') or 'locahost'
    PRINCIPAL = os.environ.get('PRINCIPAL') or 'admin'
    PASSWORD = os.environ.get('PASSWORD') or \
        'this-really-needs-to-be-changed'
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-east-1'


class Realm(Config):
    DEBUG = True


config = Realm()
