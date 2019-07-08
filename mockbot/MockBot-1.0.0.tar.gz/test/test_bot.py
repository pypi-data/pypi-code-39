#!/usr/bin/python3
# 2019-7-7

from MockBot import Bot
import pytest
import json
import os

class TestMockBot:
    user_id = os.getenv('USER_ID', None)
    bot_id = os.getenv('BOT_ID', None)
    group_id = os.getenv('GROUP_ID', None)
    api_token = os.getenv('API_TOKEN', None)

    # make instance of bot
    bot = Bot(user_id, bot_id, group_id, api_token)

    def testSendMessage(self):
        response = self.bot.sendMessage('test')
        # check for success
        assert response.status_code is 200

    def testGetResponse(self):
        msg = 'hi'
        response = self.bot.getResponse(msg)
        assert response != ''