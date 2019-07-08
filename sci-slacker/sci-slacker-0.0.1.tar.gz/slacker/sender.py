import slack


class Sender:
    def __init__(self, token, channel):
        self.client = slack.WebClient(token=token)
        self.channel = channel

    def send(self, message_blocks):
        return self.client.chat_postMessage(channel=self.channel,
                                            blocks=message_blocks)
