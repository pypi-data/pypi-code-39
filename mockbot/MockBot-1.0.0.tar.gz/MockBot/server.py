#!/usr/bin/python3
# 2019-7-7

import os
import markdown
from MockBot.bot import Bot
from flask import Flask, request

# Create instance of flask
server = Flask(__name__)
server.config['JSON_SORT_KEYS'] = False

user_id = os.getenv('USER_ID', None)
bot_id = os.getenv('BOT_ID', None)
group_id = os.getenv('GROUP_ID', None)
api_token = os.getenv('API_TOKEN', None)

# setup bot
bot = Bot(user_id, bot_id, group_id, api_token)

@server.route('/', methods=['GET'])
def index():
    try:
        markdown_file = open('README.md', 'r')
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content), 200
    except:
        return 'Project Documentation Not found', 404
        
@server.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if data is not None:
        if bot.checkUser(data):
            response = bot.getResponse(data['text'])
            if bot.sendMessage(response).status_code == 201:
                return 'Message Sent to User', 201
            else:
                return 'Error Sending Message to user', 400
        else:
            return 'Incoming message was not sent by the user; no message sent', 200
    else:
        return 'No Message Provided', 404
