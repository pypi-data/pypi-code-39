import os
import json
from util.protocol import parse_request
from threading import Lock, RLock
from pprint import pprint, pformat

class CommandContext: # TODO: replace this with an object-accessible dict
    def __init__(self, client=None):
        self.client = client
        self.authorized = None
        self.command = None
        self.header = None
        self.payload = None
        self.error = None

class ActiveUpload:
    def __init__(self, client, filename, sha1sum, size, file):
        self.client = client
        self.filename = filename
        self.sha1sum = sha1sum
        self.bytes_total = size
        self.bytes_completed = 0
        self.file = file

    def close(self):
        if self.file: self.file.close()

class CommandProcessor:
    def __init__(self, config):
        from model_controller import ModelController
        self._noisy = config.get('verbose')
        self._model = ModelController(config, self._noisy)
        self._model_lock = Lock()
        self._secret_key = config.secret_key
        self._upload_buffer_max_size = config.upload_buffer_max_size
        self._command = None
        self._commands = {}
        self._authorized_commands = set()
        self._clients = set()
        self._authorized_clients = set()
        self._active_uploads = {}
        self._handle_unknown_command = self.cmd_unknown_command
        self.register_command('authorize', self.cmd_authorize, False)
        self.register_command('ping', self.cmd_ping, True)
        self.register_command('load_image', self.cmd_load_image, True)
        self.register_command('upload_init', self.cmd_upload_init, True)
        self.register_command('upload_append', self.cmd_upload_append, True)
        # NOTE: add other commands if needed

    def print_if_noisy(self, item):
        if self._noisy:
            pprint(item, indent=2)

    def register_command(self, name, handler, require_authorization):
        self._commands[name] = handler
        if require_authorization:
            self._authorized_commands.add(name)

    def add_client(self, client):
        self._clients.add(client)
        return self.make_reply(client, 'awaiting_authorization', True)

    def remove_client(self, client):
        self._clients.discard(client)
        self._authorized_clients.discard(client)

        # Cancel and remove all pending uploads by this client
        remove = set()

        for key, upload in self._active_uploads.items():
            if upload.client is client:
                remove.add(key)
                upload.close()

        for key in remove:
            del self._active_uploads[key]

    def process_message(self, client, data):
        '''
        Decode and parse an encoded message from the client.
        Returns: context: CommandContext
        '''
        # self.print_if_noisy("Received message of type {}: {}".format(type(data), data))
        # length = len(data) if isinstance(data, bytes) else len(str(data))
        # return { 'status': 'ok', 'message': "Received message from client", 'data_type': str(type(data)), 'length': length }, True
        context = CommandContext(client)
        try:
            context.authorized = client in self._authorized_clients
            context.header, context.payload = parse_request(data)
            context.command = context.header['command']
            assert(context.command in self._commands)
        except Exception as e:
            print("Invalid request: length: {}".format(len(data)))
            print("Exception: {}".format(e))
            print("First 1000 bytes of request: ----------")
            print(data[:1000])
            print("---------------------------------------")
            context.error = e
        finally:
            return context

    def run_command(self, ctx):
        '''
        Process a parsed command as represented by the context.
        Returns: response: dict, keep_connection: bool.
        Client connection should be closed if the second returned value (keep_connection) is false.
        '''
        if ctx.error:
            return self.error_reply(ctx.client, "Invalid request"), ctx.authorized
        try:
            self.print_if_noisy("--- New message from {}: -------------------------".format(ctx.client))
            self.print_if_noisy(ctx.header)
            if ctx.command in self._authorized_commands and not ctx.authorized:
                response = self.error_reply(ctx.client, 'authorization', 'command_requires_authorization',
                    "You need to authorize to perform this command", value=ctx.command)
                return response, False

            handler = self._commands.get(ctx.command, self._handle_unknown_command)
            return handler(ctx.client, ctx.header, ctx.payload), ctx.authorized or ctx.command == 'authorize'
        except Exception as e:
            print("Exception:", e)
            print("Context:", pformat(ctx, indent=2))
            return self.error_reply(ctx.client, 'application', 'generic_error', "Internal server error"), ctx.authorized

    def make_reply(self, client, event, success, **response):
        response = response or {}
        response['event'] = event
        response['status'] = 'ok' if success else 'error'
        self.print_if_noisy('--- Sending response to {}:'.format(client))
        self.print_if_noisy(response)
        return json.dumps(response).encode()

    def error_reply(self, client, domain, code, message, **kwargs):
        return self.make_reply(client, 'error', False, message=message, domain=domain, code=code, **kwargs)

    def cmd_unknown_command(self, client, header, payload):
        return self.error_reply(client, 'application', 'invalid_command', "Command not recognized", value=header.get('command', ''))

    def cmd_authorize(self, client, header, payload):
        if header['key'] == self._secret_key:
            self._authorized_clients.add(client)
            return self.make_reply(client, 'authorize', True, message="Authorization successful")
        return self.error_reply(client, 'authorization', 'invalid_key', "Invalid secret key")

    def cmd_ping(self, client, header, payload):
        return self.make_reply(client, 'ping', True, message='pong')

    def cmd_load_image(self, client, header, payload):
        with self._model_lock:
            response = self._model.process_image(payload, header)
            response['frame_index'] = header['frame_index']
            return self.make_reply(client, 'load_image', True, **response)

    def cmd_upload_init(self, client, header, payload):
        filename = header['filename']
        savepath = 'data/uploads/{}'.format(filename)

        if filename in self._active_uploads:
            return self.error_reply(client, 'upload', 'file_exists', "A file with the same name is already being uploaded", value=filename)

        if os.path.exists(savepath):
            return self.error_reply(client, 'upload', 'file_exists', "A file with the same name already exists on the server", value=filename)

        buffer_size = min(header['max_buffer'], self._upload_buffer_max_size)
        sha1sum = header['sha1sum']

        upload = ActiveUpload(client, filename, sha1sum, header['size'], open(savepath, 'wb'))
        self._active_uploads[filename] = upload
        return self.make_reply(client, 'upload_begin', True, buffer_size=buffer_size)

    def cmd_upload_append(self, client, header, payload):
        filename = header['filename']
        upload = self._active_uploads[filename]
        upload.file.write(payload)
        upload.bytes_completed += len(payload)
        if upload.bytes_completed >= upload.bytes_total:
            upload.close()
            del self._active_uploads[filename]
            return self.make_reply(client, 'upload_append', True, finished=True, filename=upload.filename, bytes=upload.bytes_completed)
        return self.make_reply(client, 'upload_append', True, bytes=upload.bytes_completed)
