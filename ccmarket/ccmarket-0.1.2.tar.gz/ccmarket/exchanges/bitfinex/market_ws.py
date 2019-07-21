#!/usr/bin/env python3

'''
api doc
https://docs.bitfinex.com/v2/docs/ws-general
https://docs.bitfinex.com/v2/reference#ws-public-trades
'''

import asyncio
import websockets 
import json
import time

import logging

from ...base_market_ws import BaseMarketWs
from .const import WS_URL, SYMBOLS
from ...const import Channel

logger = logging.getLogger(__name__)


class MarketWs(BaseMarketWs):
    """docstring for OkexAdapter"""

    def __init__(self,exchange,symbols ,channels,listeners):
        super(MarketWs, self).__init__(exchange,symbols,channels,listeners)

        self._channelIds = {}

    
    def convert_trade(self,origin):
        price = origin[3]
        size  = origin[2]
        side  = 'sell' if origin[2] > 0 else 'buy'  
        ts    = origin[1]/1000


        # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
        # ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
        # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()

        return {
            'price':price,
            'size':size,
            'side':side,
            'ts':ts 
        }


    def convert_book_update(self,msg):

        # print(msg)

        ts = msg[2]/1000
        # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
        # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()

        # d = 'bid' if float(msg[1][0]) > 0 else 'ask'

        book = msg[1]
        if book[1] >0:
            if book[2] > 0:
                
                return {
                    "bid":[book[0] , book[2]],
                    "ts":ts
                }
            else :
                return {
                    "ask":[book[0] , -book[2]],
                    "ts":ts
                }
        else:
            if book[2] > 0:
                return{
                    "bid":[book[0] , 0],
                    "ts":ts
                    
                }
            else:
                return {
                    "ask":[book[0] , 0],
                    "ts":ts
                }   


    def convert_book_snapshot(self,msg):

        asks = []
        bids = []

        data = msg[1]
        for line in data:
            if line[1] > 0:
                if line[2] >0:
                    bids.append([line[0],line[2]])
                else:
                    asks.append([line[0],-line[2]])

        return {
            "asks":asks,
            "bids":bids
            }


    async def connect(self ):
 
        logger.info(f"bitfinex,will connect to:{WS_URL}")
        
        async with websockets.connect(WS_URL) as websocket:

            last_ts = None
            current_ts = None
            
            self._listener.on_start()

            try:

                # info message from server
                res = await websocket.recv()
                
                logger.info(f"bitfinex,recv flag:{res}")
                
                self._listener.on_recv(res)

                conf = { 
                    "event": "conf", 
                    "flags": 32768
                }

                await websocket.send(json.dumps(conf))
                self._listener.on_sent(json.dumps(conf))

                if Channel.trade in self._channels:
                    for symbol in self._symbols:

                        s = 't%s%s' % (symbol[0].upper(),symbol[1].upper()) 

                        req = { "event": "subscribe", "channel": "trades", "symbol": s}
                    
                        await websocket.send(json.dumps(req))

                        self._listener.on_sent(json.dumps(req))

                if Channel.book in self._channels:
                    for symbol in self._symbols:

                        s = 't%s%s' % (symbol[0].upper(),symbol[1].upper()) 

                        req = { "event": "subscribe", "channel": "book", "symbol": s,"len":100}
                    
                        await websocket.send(json.dumps(req))

                        self._listener.on_sent(json.dumps(req))
                
                logger.info('bitfinex,start recv loop.')
                
                while True:

                    res = await websocket.recv()
                    self._listener.on_recv(res)

                    # timer.refresh()
     

                    line = json.loads(res)

                    if isinstance(line,dict) and line.get('event') == 'pong':
                        logger.info('bitfinex,recv pong ..')

                        continue

                    if isinstance(line,dict) and line.get('event') == 'subscribed':

                        logger.info(f"bitfinex,subscribed:{line}" )
                        
            
                        symbol = line.get('symbol')
                        coin = symbol[1:4].lower()
                        currency = symbol[4:7].lower()

                        channel = None
                        if 'trades' == line.get('channel'):
                            channel = Channel.trade
                        elif 'book' == line.get('channel'):
                            channel = Channel.book


                        self._channelIds[line.get('chanId')] = {
                            'channel':channel,
                            'coin': coin,
                            'currency':currency
                        }
                        
                        logger.info(f"bitfinex,channel ids:{self._channelIds}")
                        
                        # for subscribe in self.subscribes:
                        #     if line.get('channel') == subscribe.get('channel') and line.get('symbol') == subscribe.get('symbol') :
                        #         subscribe['chanId'] = line.get('chanId')

                    elif isinstance(line,list):
 

                        # for subscribe in self.subscribes:
                        #     if line[0] == subscribe.get('chanId'):
                        #         cb = subscribe.get('callback')

                        #         cb(line , subscribe.get('coin') , subscribe.get('currency'))


                        channelId = line[0]

                        channelObj = self._channelIds.get(channelId)
                        coin = channelObj.get('coin')
                        currency = channelObj.get('currency')
                        channel = channelObj.get('channel')


                        if Channel.book == channel:
                            # asks = []
                            # bids = []


                            # for item in channelMsg:
                            #     if item[2] > 0:
                            #         bids.append([item[0],item[2],item[1]])
                            #     else:
                            #         asks.append([item[0],-item[2],item[1]])

                            # print('asks:' , asks, 'bids:' , bids)

                            if isinstance(line[1],list):
                                    

                                

                                ts = line[2]/1000
                                current_ts = int(ts/3600)


                                if isinstance(line[1][0],list):
            
                                    item = line

                                    converted = self.convert_book_snapshot(item)

                                    self._listener.on_resolve(coin,currency,channel.value + '/snapshot',None,ts,item)
                                    self._listener.on_book_snapshot(coin,currency,ts,converted)



                                else:

                                    item = line

                                    converted = self.convert_book_update(item)
                                    
                                    self._listener.on_resolve(coin,currency,channel.value + '/update',None,ts,item)
                                    self._listener.on_book_update(coin,currency,ts,converted)






                        elif Channel.trade == channel:
                            
                            item2 = line[1]

                            if isinstance(item2,str):
                                
                                if 'tu'==item2:

                                    item = line[2]

                                    tid = item[0]
                                    ts = item[1]/1000
                                    current_ts = int(ts/3600)


                                    converted = self.convert_trade(item)

                                    self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                                    self._listener.on_trade(coin,currency,ts,converted)


                                    
                            elif isinstance(item2,list):
                                channelMsg = item2

                                
                                for item in channelMsg:

                                    tid = item[0]
                                    ts = item[1]/1000
                                    current_ts = int(ts/3600)

                                    converted = self.convert_trade(item)

                                    self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                                    self._listener.on_trade(coin,currency,ts,converted)

                    
                    if last_ts and current_ts and current_ts > last_ts:
                            self._listener.on_flag(last_ts*3600)

                    last_ts = current_ts  

            except websockets.ConnectionClosed as e:
                self._listener.on_end()
                logger.warning(str(e))

                raise
            except Exception as e:

                logger.info(f'time:{time.time()}')
                logger.error(str(e))

                raise

    # unsubscribe channels
    async def unsubscribe_without_login(self,url, channels):
        pass
        # async with websockets.connect(url) as websocket:
        #     sub_param = {"op": "unsubscribe", "args": channels}
        #     sub_str = json.dumps(sub_param)
        #     await  websocket.send(sub_str)
        #     # logger.debug(f"send: {sub_str}")
        #
        #     res = await websocket.recv()
        #     res = inflate(res)
        #     # logger.debug(f"{res}")

if __name__ == '__main__':
 
    pass





