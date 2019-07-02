class TelegramError(Exception):
    def __init__(self, message):
        super(TelegramError, self).__init__()
        self.message = message

    def __str__(self):
        return '%s' % self.message


class InvalidToken(TelegramError):
    def __init__(self):
        super(InvalidToken, self).__init__('Invalid token')


class InvalidChatId(TelegramError):
    def __init__(self):
        super(InvalidChatId, self).__init__('Invalid chat id')


class InvalidMessage(TelegramError):
    def __init__(self):
        super(InvalidMessage, self).__init__('Message cannot be empty')
