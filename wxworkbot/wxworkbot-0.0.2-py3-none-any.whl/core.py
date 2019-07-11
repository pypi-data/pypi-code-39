# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64
import hashlib
import logging
import os

import requests

from wxworkbot.exceptions import HookValidationError

logger = logging.getLogger()


class Bot(object):
    """
    encapsulate api, see: https://work.weixin.qq.com/api/doc?notreplace=true#90000/90135/91760
    """
    BASE_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='

    @staticmethod
    def __get_uri(key: str) -> str:
        """
        concatenate the uri
        :param key: the key of web hook
        :return: uri
        """
        return Bot.BASE_URL + key

    @staticmethod
    def _validate(uri: str) -> bool:
        """
        validate web hook
        :param uri:
        :return: is valid or not
        """
        try:
            resp = requests.options(uri)
            # check error response
            if resp.status_code != 200:
                logger.error('error response! status_code: %d', resp.status_code)
                return False

            # check invalid web hook
            errcode = resp.json().get('errcode', 0)
            if errcode == 93000:
                logger.error('invalid web hook: %s', uri)
                return False

        except Exception as e:
            logger.error('unexpected error occurs: %s', e)
            return False

        return True

    def __init__(self, bot_name: str, key: str):
        """
        :param bot_name: used for logging, in provision of a better semantics
        :param key: web hook key
        """
        self.bot_name = bot_name
        self.uri = Bot.__get_uri(key)
        if not Bot._validate(self.uri):
            raise HookValidationError("invalid web hook key: %s" % key)

    def _send_msg(self, msg_body: dict):
        """
        send message post action
        :param msg_body: json
        :return:
        """
        resp = requests.post(self.uri, json=msg_body)
        logger.debug('response status code: %d, response body: %s', resp.status_code, resp.text)

    def send_text(self, text: str):
        """
        a simplified method without mentioned list
        :param text: plain text
        :return:
        """
        self.send_text_with_mentioned(text, [])

    def send_text_with_mentioned(self, text: str, mentioned_list: list):
        """
        send text message
        :param text: plain text
        :param mentioned_list: mentioned names in list
        :return:
        """
        msg_body = {
            "msgtype": "text",
            "text": {
                "content": text,
                "mentioned_list": mentioned_list,
            }
        }
        logger.info("[%s]send text %s", self.bot_name, text)
        self._send_msg(msg_body)

    def send_image(self, image_path: str):
        """
        send image message
        :param image_path: image path
        :return:
        """
        if not os.path.exists(image_path):
            logger.error("path not exists:%s " % image_path)
            return

        with open(image_path, 'rb') as f:
            raw_content = f.read()
            self.send_image_bytes(raw_content)

    def send_image_bytes(self, image: bytes):
        raw_md5 = hashlib.md5(image).hexdigest()
        encoded_content = str(base64.b64encode(image), 'utf-8')
        msg_body = {
            "msgtype": "image",
            "image": {
                "base64": encoded_content,
                "md5": raw_md5
            }
        }
        logger.info("[%s]send text %s" % (self.bot_name, image_path))
        self._send_msg(msg_body)

    def send_markdown(self, content: str):
        """
        send markdown message
        :param content: content in plain text
        :return:
        """
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        logger.info("[%s]send markdown message %s" % (self.bot_name, content))
        self._send_msg(msg)
