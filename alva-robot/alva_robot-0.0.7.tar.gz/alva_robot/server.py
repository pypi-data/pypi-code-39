# coding=utf8

__author__ = 'Alexander.Li'

import uuid
import json
import pollworker
import logging
from secp256k1py import secp256k1
from errorbuster import formatError
from .functions import Aws


def load_config():
    with open('.broker_config', 'r') as f:
        return json.loads(f.read())


class Server(object):
    def __init__(self):
        self.config = load_config()
        self.aws = Aws(self.config)

    def poll(self):
        messages = self.aws.recv(self.config.get('ID'))
        if messages.get('Messages'):
            return {'messages': messages.get('Messages'), 'config': self.config}
        else:
            logging.info('got no message')


class Command(object):
    def __init__(self, commandDict):
        self.data = commandDict

    @property
    def unique_id(self):
        return self.data.get('unique_id')

    @property
    def name(self):
        return self.data.get('name')

    @property
    def params(self):
        return self.data.get('params')


class Message(object):
    def __init__(self, messageDict):
        self.data = messageDict

    @property
    def unique_id(self):
        return self.data.get('unique_id')

    @property
    def content_type(self):
        return self.data.get('content-type')

    @property
    def action(self):
        return self.data.get('action')

    @property
    def text(self):
        if self.content_type == "text":
            return self.data.get('body').get('content')
        return ''


class Sender(object):
    def __init__(self, senderDict):
        self.data = senderDict

    @property
    def host_id(self):
        return self.data.get('host_id')

    @property
    def user_id(self):
        return self.data.get('user_id')

    @property
    def nick_name(self):
        return self.data.get('nick_name')

    @property
    def avatar(self):
        return self.data.get('avatar')

    @property
    def public_key(self):
        return self.data.get('public_key')

    @property
    def endpoint(self):
        return self.data.get('endpoint')


class MRequest(object):
    def __init__(self, raw_message):
        self.data = json.loads(raw_message)
        self.sender = Sender(self.data.get('sender'))
        if "content" in self.data:
            self.message = Message(self.data.get('content'))
        else:
            self.message = None
        if "command" in self.data:
            self.command = Command(self.data.get('command'))
        else:
            self.command = None


def send_command_to(config, aws, target, response):
    resp = response.make_response(config, aws, target.get('public_key'))
    logging.info(aws.send_msg(target.get('endpoint'), json.dumps(resp.data)))


class Response(object):
    def __init__(self, basic_dict):
        self.data = basic_dict

    def make_response(self, config, aws, target_public):
        self.data.update(
            {
                'sender': {
                    'host_id': 'miaomi',
                    'user_id': config.get('ID'),
                    'nick_name': config.get('NICK'),
                    'avatar': config.get('AVATAR'),
                    'public_key': config.get('BROKER_PUBLIC'),
                    'endpoint': aws.with_url(config.get('ID'))
                }
            }
        )
        keypair = secp256k1.make_keypair()
        targetPublicKey = secp256k1.PublicKey.restore(target_public)
        enced = targetPublicKey.encrypt(keypair.privateKey, json.dumps(self.data).encode())
        return {
            'encoded': enced.get('enc'),
            'iv': enced.get('iv'),
            'public_key': "%s" % keypair.publicKey,
            'cipher': 'secp256k1'
        }


class MessageResponse(Response):
    def __init__(self, text):
        message = {
            'content': {
                'unique_id': uuid.uuid4().hex,
                'content-type': 'text',
                'action': 'new',
                'body': {
                    'content': text
                }
            }
        }
        super(MessageResponse, self).__init__(message)


class CommandResponse(Response):
    def __init__(self, name, *params):
        command = {
            'command': {
                'name': name,
                'params': params
            }
        }
        super(CommandResponse, self).__init__(command)


class ContackResponse(Response):
    def __init__(self, users):
        message = {
            'content': {
                'unique_id': uuid.uuid4().hex,
                'content-type': 'contacts',
                'action': 'new',
                'body': {
                    'contacts':[
                        {
                            'id': user.get('user_id'),
                            'nick_name': user.get('nick_name'),
                            'avatar': user.get('avatar')
                        }
                        for user in users
                    ]
                }
            }
        }
        super(ContackResponse, self).__init__(message)


executors = {}


MESSAGE_HANDLER = 'MESSAGE_HANDLER'


def api(cmd_name):
    def decorator(f):
        executors[cmd_name] = f
        return f
    return decorator


def worker(pid, message):
    messages = message.get('messages')
    config = message.get('config')
    aws = Aws(config)
    for msg in messages:
        body = json.loads(msg.get('Body'))
        privateKey = secp256k1.PrivateKey.restore(config.get('BROKER_PRIVATE'))
        publicKey = secp256k1.PublicKey.restore(body.get('public_key'))
        iv = body.get('iv')
        enc = body.get('encoded')
        try:
            raw = privateKey.decrypt(publicKey, enc, iv)
            req = MRequest(raw)
        except Exception as e:
            logging.error(formatError(e))
        finally:
            aws.rm_msg(config.get('ID'), msg.get('ReceiptHandle'))
        resp = None
        if req.command:
            if req.command.name in executors:
                resp = executors[req.command.name](config, aws, req)
        if req.message:
            if req.message.action == "new":
                if MESSAGE_HANDLER in executors:
                    resp = executors[MESSAGE_HANDLER](config, aws, req)
        if resp:
            response_text = json.dumps(resp.make_response(config, aws, req.sender.public_key))
            logging.info(aws.send_msg(req.sender.endpoint, response_text))
            logging.info('message sended!')


def start():
    pollworker.regist_worker(worker)
    pollworker.regist_poller(Server())
    pollworker.start()
