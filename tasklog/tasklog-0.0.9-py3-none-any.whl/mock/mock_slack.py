
class MockSLACK:
    def __init__(self):
        self.instance = None

    def connect(self, slackAPIToken):
        pass

    def isConnected(self):
        return True

    def postMessage(self, channelName, message):
        response = {
            'ok': True
        }
        return response
