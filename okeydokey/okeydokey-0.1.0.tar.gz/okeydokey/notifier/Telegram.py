import logging

from .notifier import Notifier
from time import sleep
import telegram.bot


class Telegram(Notifier):
    _name = 'Telegram'
    token = str()

    def notify(self, message):
        if not self.configuration_validated:
            logging.critical('Configuration must be validated before any message is sent')
            return False
        messenger = telegram.bot.Bot(self.configuration['credentials']['token'])
        _composed_message = f'[NOTARY: {self.configuration["name"]}] ' + message
        _responses = []
        for user in self.configuration['target']:
            _responses.append(messenger.send_message(chat_id=str(user), text=_composed_message))
            sleep(1)
        del messenger
        logging.critical(f'Message sent: {_composed_message} to {self.configuration["target"]}')
        return _responses

    def validate_configuration(self):
        if 'name' not in self.configuration:
            raise ValueError(
                "No 'name' found in configuration. It is required in order to report which key has been retrieved."
            )
        if self.configuration.get('type') != 'Telegram':
            raise ValueError("Notification backend instance and notification type mismatch:"
                             f" {self.configuration.get('type')} != Telegram")
        if 'credentials' not in self.configuration:
            raise ValueError("No credentials found in configuration")
        if 'token' not in self.configuration['credentials']:
            raise ValueError("No Telegram token found in configuration under credentials section")
        if 'target' not in self.configuration:
            raise ValueError("No Telegram target found in configuration file")
        if type(self.configuration['target']) != list:
            raise ValueError("Telegram target configuration must be an array")
        self.configuration_validated = True
        return True
