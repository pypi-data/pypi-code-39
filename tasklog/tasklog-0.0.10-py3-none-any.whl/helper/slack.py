import slack


class SLACK2:
    def __init__(self):
        self.instance = None
        self.apiToken = None

    def connect(self, slackAPIToken):
        self.apiToken = slackAPIToken
        self.instance = slack.WebClient(token=slackAPIToken)

    def isConnected(self):
        return self.instance is not None

    def postMessage(self, channelName, message, asUser=True):
        isPostedAsUser = "true" if asUser else "false"
        channelID = self._getChannelIDByChannelName(channelName)

        if channelID is not None:
            response = self.instance.chat_postMessage(channel=channelID, text=message, as_user=isPostedAsUser,
                                                      mrkdwn="true")
            return response

        return None

    def _getChannelIDByChannelName(self, channelName):

        channelTypes = "public_channel, private_channel"
        hasMoreChannels = True
        cursorID = None

        while hasMoreChannels:
            if cursorID is None:
                response = self.instance.conversations_list(token=self.apiToken, exclude_archived="true",
                                                            exclude_members="true",
                                                            limit=100, types=channelTypes)
            else:
                response = self.instance.conversations_list(token=self.apiToken, exclude_archived="true",
                                                            exclude_members="true",
                                                            limit=100, types=channelTypes, cursor=cursorID)

            if not response['ok']:
                return None

            meta = response.data['response_metadata']
            hasMeta = meta is not None
            cursorID = meta['next_cursor'] if hasMeta and meta['next_cursor'] is not None else None
            cursorID = None if cursorID is '' else cursorID
            hasMoreChannels = cursorID is not None

            channels = response.data['channels']
            channelIDs = [data['id'] for data in channels if data['is_channel'] and data['name'] == channelName]

            if len(channelIDs) == 0:
                continue

            channelID = channelIDs[0]
            return channelID

        return None
