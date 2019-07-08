#!/usr/bin/python3
# 2019-7-7

import re
import requests
from spongemock.spongemock import mock

class Bot:
    def __init__(self, user_id, bot_id, group_id, api_token):
        self.bot_id = bot_id
        # This is the user ID of the person who should be "mocked"
        self.user_id = user_id
        self.group_id = group_id
        self.api_token = api_token
        self.api_base_url = 'https://api.groupme.com/v3'
        self.api_session = requests.session()

       
    def sendMessage(self, msg):
        """Send a message from the bot to its assigned group.
        Parameters
        ----------
        msg : string 
            message to be sent to group
        Returns
        -------
        response : response
            the response object returned by the API call
        """
        # set parameters for post request
        params = {
            'bot_id': self.bot_id,
            'text': msg
        }
        # send the request to the api and get the results in the response var
        response = self.api_session.post(
            f'{self.api_base_url}/bots/post', 
            params=params
        )
        return response
        
    def checkUser(self, callback):
        """ Check if the message sent was by the targeted user
        Parameters
        ----------
        callback : object
            - The Request object sent to the server 
        Returns
        -------
        boolean
            True if the user who sent the message is the targeted user
            False otherwise
        """
        return callback['user_id'] == self.user_id
         
        
    def getResponse(self, msg):
        """Given a message the appropriate response is returned.
        Parameters
        ----------
        msg : string
            a message to respond to "mockify"
        Returns
        -------
        response : string 
            The bot's response to the users message
        """
        # makes a call to the sponegemock package to make the resposne
        return mock(msg)