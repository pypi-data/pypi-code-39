import json
import os
import tempfile
import unittest
from collections import namedtuple

import configparser
from mock import patch

import beves
from beves.errors import InvalidChatId, InvalidToken, TelegramError


class TestBeves(unittest.TestCase):
    def setUp(self):
        beves.config = configparser.ConfigParser()
        self.tempconfig = tempfile.mktemp()

    def tearDown(self):
        try:
            os.unlink(self.tempconfig)
        except:
            pass

    def test_config(self):
        open(self.tempconfig, 'w').write('''
        [beves]
        token = 123456:abcdecv
        chat_id = 12345
               ''')
        beves.__main__.load_config(self.tempconfig)
        bot = beves.Beves()
        self.assertIsInstance(bot, beves.Beves)

    def test_arguments(self):
        bot = beves.Beves('123456:abcdecv', '123456')
        self.assertIsInstance(bot, beves.Beves)

        beves.Beves(token='123456:abcdecv')
        self.assertIsInstance(bot, beves.Beves)

        beves.Beves(chat_id='12134')
        self.assertIsInstance(bot, beves.Beves)

        with self.assertRaises(InvalidChatId):
            beves.Beves(chat_id='12fe134')

        with self.assertRaises(InvalidToken):
            beves.Beves(token='askaskaskjka')

        with self.assertRaises(TelegramError):
            bot = beves.Beves('123456:abcdecv', 1111111111)
            bot.push('test')

    def test_push(self):
        data = self._json2obj('{"ok":true}')
        with patch('requests.post', return_value=data):
            bot = beves.Beves('123456:abcdecv', '123456')
            self.assertTrue(bot.push('test'))

    @staticmethod
    def _json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())

    def _json2obj(self, data):
        return json.loads(data, object_hook=self._json_object_hook)


if __name__ == '__main__':
    unittest.main()
