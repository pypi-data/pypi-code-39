import os

COUCHDB_DB = os.environ.get('COUCHDB_DB', 'numbers')
COUCHDB_USER = os.environ.get('COUCHDB_USER', 'admin')
COUCHDB_PASSWORD = os.environ.get('COUCHDB_PASSWORD', '110889QAZ')

COUCHDB_DOMAIN = os.environ.get('COUCHDB_DOMAIN', 'couchdb')
COUCHDB_PORT = os.environ.get('COUCHDB_PORT', '5984')

COUCHDB_URI = f'http://{COUCHDB_USER}:{COUCHDB_PASSWORD}@{COUCHDB_DOMAIN}:{COUCHDB_PORT}/'
