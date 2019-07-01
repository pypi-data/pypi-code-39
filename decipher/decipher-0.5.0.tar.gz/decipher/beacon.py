#!/usr/bin/env python
"""
Decipher Beacon 2.0 API access library
"""

# The API version we'll be accessing
from ConfigParser import RawConfigParser, NoSectionError, DuplicateSectionError
from functools import partial
import hmac
import json
import os, requests
import pwd
import datetime
import simplejson
import sys

KEYLEN = 32
DEFAULT_HOST = "v2.decipherinc.com"

def date_to_isoformat(o):
    # convert local timestap to iso8601 format
    # apparently this is how to do it without requiring the pytz module installed
    return datetime.datetime.utcfromtimestamp(int(o.strftime("%s"))).isoformat() + 'Z'

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return date_to_isoformat(o)


class BeaconAPIException(Exception):
    def __init__(self, code, message, body=None):
        self.code, self.message, self.body = code, message, body
        Exception.__init__(self, "%s: %s" % (code, message))

class BeaconAPI(object):
    verbose = xml = False
    version = 'v1'
    section = 'main'    # name of section in INI file we are using

    def __init__(self, host=None, key=None):
        self.host, self.key = host, key

    def _debug(self, what):
        if self.verbose:
            print >> sys.stderr, what


    def login(self, key, host=DEFAULT_HOST):
        """
        Set the API key and optionally the API host.
        :param key: a 32-characters long retrieved from your API keys page
        :param host: optional; uses v2.decipherinc.com if not specified
        :return:
        """
        assert len(key) == KEYLEN, "API key specified is not exactly %d characters long" % KEYLEN
        self.key, self.host  = key, host

    @property
    def inifile(self):
        return os.path.expanduser("~/.config/decipher")

    @property
    def parser(self):
        parser = RawConfigParser()
        parser.read(self.inifile)
        return parser

    def _load(self, section):
        "attempt to load key data from ~/.config/decipher file"
        parser = self.parser
        try:
            key = parser.get(section, 'key')
            host = parser.get(section, 'host')
        except NoSectionError:
            raise KeyError
        return key, host

    def _save(self, section, key, host):
        parser = self.parser
        try:
            parser.add_section(section)
        except DuplicateSectionError:
            pass
        parser.set(section, "key", key)
        parser.set(section, "host", host)
        parser.write(open(self.inifile, "w"))
        os.chmod(self.inifile, 0600)


    def _ensureKey(self):
        "Ensure key / host are configured"
        if self.host is None:
            if 'BEACON_KEY' in os.environ:
                self.key = os.environ['BEACON_KEY']
                self.host = os.environ.get('BEACON_HOST') or 'v2.decipherinc.com'
                if not self.host.startswith('http'):
                    self.host = 'https://%s' % self.host

            # BEACON_KEY & BEACON_HOST specified?
            elif 'HERMES2_HOME' in os.environ:
                self._debug("+ HERMES2_HOME set, trying to call v2conf")
                try:
                    ekey, self.host = map(str.strip, os.popen("here v2conf localapi localurl").readlines())
                except ValueError:
                    raise BeaconAPIException(500, "Could not call v2conf to determine local API key")
                self._debug('+ v2conf response: %r / %r' % (ekey, self.host))
                if len(ekey) != 64:
                    raise BeaconAPIException(500, "Invalid local API key")

                # convert key to API key
                username = pwd.getpwuid(os.getuid()).pw_name
                self.key = 'local %s %s' % (username, hmac.new(ekey, username).hexdigest())
            else:
                try:
                    self.key, self.host = self._load(self.section)
                except KeyError:
                    raise BeaconAPIException(code=500, message="No key has been defined in environment. Either use 'beacon login' or set BEACON_KEY and optionally BEACON_HOST")


    def do(self, action, name, args):
        "Perform action"
        self._ensureKey()
        url = '%s/api/%s/%s' % (self.host, self.version, name)
        self._debug('> %s %s' % (action.upper(), url))
        self._debug('>> x-apikey: %s' % self.key)

        kw = {}
        if action == 'get':
            kw['params'] = args
        else:
            kw['data'] = simplejson.dumps(args)
        headers = {"x-apikey" : self.key, 'content-type': 'application/json'}
        if self.xml:
            headers['accept'] = 'application/xml'
        r = requests.request(action, url, verify=True, headers=headers, **kw)
        self._debug('<< %s %s' % (r.status_code, r.reason))
        if 'x-typehint' in r.headers:
            self._debug('< x-typehint: %s' % r.headers['x-typehint'])
        if r.status_code != 200:
            raise BeaconAPIException(code=r.status_code, message=r.reason, body=r.content)
        if r.headers['content-type'] == 'application/json':
            return r.json()
        return r.content

    def get(self, _name, **args):      return self.do('get', _name, args)
    def post(self, _name, **args):     return self.do('post', _name, args)
    def put(self, _name, **args):      return self.do('put', _name, args)
    def delete(self, _name, **args):   return self.do('delete', _name, args)


api = BeaconAPI()
