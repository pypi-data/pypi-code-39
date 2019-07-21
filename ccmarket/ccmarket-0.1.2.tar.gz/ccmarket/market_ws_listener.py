import time
import json
import hashlib
import logging

from .base_listener import BaseListener

logger = logging.getLogger(__name__)


class MarketWsListener(BaseListener): 
    def __init__(self,ex,listeners):
        super(MarketWsListener, self).__init__(ex)
       
        self._listeners = listeners

    def on_sent(self,plain):
        
        logger.debug(f"{self._exchange},send:{plain}")

        for listener in self._listeners:
            listener.on_sent(plain)

    def on_recv(self,plain):

        logger.debug(f"{self._exchange},recv:{plain}" )

        for listener in self._listeners:
            listener.on_recv(plain)
        
    def on_start(self):

        logger.info(f"{self._exchange},connected" )

        for listener in self._listeners:
            listener.on_start()

        
    def on_end(self):

        logger.info(f"{self._exchange},disconnect")

        for listener in self._listeners:
            listener.on_end()

    def on_resolve(self,coin,currency,channel,cid,ts,detail):

        logger.debug(f"{self._exchange},{coin},{currency},{channel},{cid},{ts},{detail}" )

        for listener in self._listeners:
            listener.on_resolve(coin,currency,channel,cid,ts,detail)


    def on_trade(self,coin,currency,ts,detail):

        logger.debug(f"{self._exchange},{coin},{currency},{ts},{detail}" )

        for listener in self._listeners:
            listener.on_trade(coin,currency,ts,detail)

    def on_book_update(self,coin,currency,ts,detail):

        logger.debug(f"{self._exchange},{coin},{currency},{ts},{detail}" )

        for listener in self._listeners:
            listener.on_book_update(coin,currency,ts,detail)

    def on_book_snapshot(self,coin,currency,ts,detail):

        logger.debug(f"{self._exchange},{coin},{currency},{ts},{detail}" )


        for listener in self._listeners:
            listener.on_book_snapshot(coin,currency,ts,detail)

    def on_flag(self,ts):

        logger.debug(f"running flag,{self._exchange},{ts}" )

        for listener in self._listeners:
            listener.on_flag(ts)

