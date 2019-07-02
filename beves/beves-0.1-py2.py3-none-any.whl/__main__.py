from __future__ import print_function

import argparse
import json
import logging
import os.path
import sys

import configparser
import requests
from builtins import input

from beves.metadata import __version__, __description__
from beves.errors import InvalidToken, InvalidChatId, InvalidMessage, TelegramError

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config_name = os.path.expanduser('~/.beves')


class Beves:
    def __init__(self, token=None, chat_id=None, base_url=None):
        if not token or not chat_id:
            if not hasattr(config, '_loaded'):
                load_config()
            if not config.sections():
                raise Exception('No configuration found')
            if not token:
                token = config['beves']['token']
            if not chat_id:
                chat_id = config['beves']['chat_id']
        if base_url is None:
            base_url = 'https://api.telegram.org/bot'

        self.token = self._validate_token(token)
        self.chat_id = self._validate_chat_id(chat_id)
        self.base_url = str(base_url) + str(self.token)
        write_config(self.token, self.chat_id)

    def push(self, message=None, parse_mode=None, disable_web_page_preview=None):
        if not message and not hasattr(config, '_loaded'):
            raise InvalidMessage()
        elif not message:
            message = config['beves']['default_message']

        url = '{0}/sendMessage'.format(self.base_url)
        data = {'chat_id': self.chat_id, 'text': message}

        if parse_mode:
            data['parse_mode'] = parse_mode
        if disable_web_page_preview:
            data['disable_web_page_preview'] = disable_web_page_preview

        req = requests.post(url, json=data)

        if req.ok:
            logger.info('Message pushed to {chat_id}'.format(message=message, chat_id=self.chat_id))
            return True
        else:
            error = json.loads(req.text)['description']
            raise TelegramError(error)

    @staticmethod
    def _validate_token(token):
        if any(x.isspace() for x in token):
            raise InvalidToken()

        left, sep, _right = token.partition(':')
        if (not sep) or (not left.isdigit()) or (len(left) < 3):
            raise InvalidToken()

        return token

    @staticmethod
    def _validate_chat_id(chat_id):
        try:
            chat_id = int(chat_id)
        except Exception:
            raise InvalidChatId()
        return chat_id


def load_config(filename=None):
    if filename is None:
        filename = config_name
    config.read(filename)
    config._loaded = True


def write_config(token, chat_id):
    config['beves'] = {'token': token, 'chat_id': chat_id, 'default_message': 'task finished'}
    with open(config_name, 'w') as configfile:
        config.write(configfile)


def read_from_stdi():
    stdin = []
    if not sys.stdin.isatty():
        stdin = sys.stdin.read().splitlines()
    return stdin


def parse_args():
    parser = argparse.ArgumentParser(
        description=__description__)
    parser.add_argument("-t", "--token", help="telegram bot token")
    parser.add_argument("-i", "--chat_id", help="sender chat id")
    parser.add_argument("-c", "--config", help="configuration file instead of {config}".format(config=config_name))
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument("message", nargs="*", help="Message to send")

    _args = parser.parse_args()

    return _args


def main():
    try:
        args = parse_args()
        token = args.token
        chat_id = args.chat_id
        if not os.path.isfile(config_name):
            if token is None:
                token = input("Token: ")
            else:
                token = args.token
            if chat_id is None:
                chat_id = input("Chat ID: ")
            else:
                chat_id = args.chat_id
        elif args.config:
            token = ''
            chat_id = ''
            load_config(args.config)
        if not args.message:
            message = ' '.join(read_from_stdi())
        else:
            message = ' '.join(args.message)
        beves = Beves(token, chat_id)
        beves.push(message)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
