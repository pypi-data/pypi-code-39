import getpass
from playhouse.sqlcipher_ext import *
import os

passphrase = getpass.getpass('Autentiquese: ')
userDir=os.getenv("HOME")
database = SqlCipherDatabase(userDir+'/.config/shortcuts/connections.db', passphrase=passphrase)

from peewee import *
from datetime import date
class Organizations(Model):
    name = CharField()
    alias = CharField()
    class Meta:
        database=database

class Services(Model):
    organization = IntegerField()
    host = CharField()
    type = IntegerField()
    username = CharField()
    password = CharField()
    port = CharField()
    key = IntegerField()
    class Meta:
        database=database

class Types_service(Model):
    name = CharField()
    class meta:
        database=database

class Keys(Model):
    public = CharField()
    private = CharField()
    class Meta:
        database=database
