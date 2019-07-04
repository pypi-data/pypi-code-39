import requests
import os
import time
import datetime
import socket
import types
from functools import wraps


class NtfBot:
    """
    A python bot for sending function running message to my telegram account.
    """
    def __init__(self, bot_token=None, bot_chatID=None):
        if not bot_token:
            self.bot_token = os.getenv("JUPYBOT_TOKEN")
            if not self.bot_token:
                raise AttributeError('can\'t find bot_token from env variable')
        else:
            self.bot_token = bot_token

        if not bot_chatID:
            self.bot_chatID = os.getenv("JUPYBOT_CHATID")
            if not self.bot_chatID:
                raise AttributeError('can\'t find bot_chatID from env variable')
        else:
            self.bot_chatID = bot_chatID


    def __call__(self, code_message="Code execution finished"):
        try:
            msg = '\"'+code_message+ '\" from ' + socket.gethostname() +\
                ' at ' + str(datetime.datetime.now())
            self._telegram_bot_sendtext(msg)
        except Exception as e:
            print(e)
        pass


    @staticmethod    
    def _telegram_bot_sendtext(bot_message):
        
        bot_token = '868875198:AAEbmuyzBdu3BK-h2pKuCc9vVFNGzE0WqlY'
        bot_chatID = '313426050'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)
        
        res_dict = response.json()
        if res_dict['ok'] == True:
            print("Message sent successfully")
        else:
            print("Message sent failed. Check network, bot_tocken or chat id")


class NtbMark:
    def __init__(self, func):
        wraps(func)(self)
        self.nb = NtfBot()

    def __call__(self, *args, **kwargs):
        t0 = time.time()
        res = self.__wrapped__(*args, **kwargs)
        t = time.time()-t0
        msg = f'function \'{self.__name__}\' cost {t}s'
        self.nb(msg)
        return res 

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)



if __name__=='__main__':
    @NtbMark
    def add(x,y):
        return x+y

    add(1,1)
    nb = NtfBot()
    nb('hello')