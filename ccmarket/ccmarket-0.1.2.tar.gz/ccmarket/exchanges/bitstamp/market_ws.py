#!/usr/bin/env python3
'''
api doc
https://www.bitstamp.net/websocket/v2/
'''

import aiohttp
import websockets 
import json
import re
import logging

from ...const import Channel
from ...base_market_ws import BaseMarketWs
from .const import WS_URL,SYMBOLS ,SYNC_BOOK_URL

CHANNELS={
    Channel.trade:'ticker',
    Channel.book:'book'
}


logger = logging.getLogger(__name__)


class MarketWs(BaseMarketWs):
    """docstring for OkexAdapter"""

    def __init__(self,exchange,symbols,channels ,listeners):
        super(MarketWs, self).__init__(exchange,symbols,channels,listeners)
        
    def convert_trade(self,origin):
        price = origin.get('price_str')
        size  = origin.get('amount_str')
        side  = 'buy' if origin.get('type')== 0 else 'sell'  
        ts    = float(origin.get('microtimestamp'))/1000000

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
        bids = msg.get('bids')
        asks = msg.get('asks')

        ts = float(msg.get('microtimestamp'))/1000000

        # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
        # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()


        # lines = []

        # for bid in bids:
        #     lines.append([str(ts),str(bid[0]),str(bid[1]),'bid'])
        # for ask in asks:
        #     lines.append([str(ts),str(ask[0]),str(ask[1]),'ask'])

        return {
            "asks":asks,
            "bids":bids,
            "ts":ts
        }
        
    def convert_book_snapshot(self,msg):

        bids = msg.get('bids')
        asks = msg.get('asks')

        return{
            "bids":bids,
            "asks":asks
        }

    async def connect(self):
        
        logger.info(f"bitstamp,will connect to:{WS_URL}")
        
        async with websockets.connect(WS_URL) as websocket:
            
            last_ts = None
            current_ts = None

            self._listener.on_start()

            try:

                # res = await websocket.recv()

                # print('flag:',res)

                for channel in self._channels:
                    for symbol in self._symbols:

                        if channel == Channel.trade:

                            req = {
                                "event": "bts:subscribe",
                                "data":{"channel": f"live_trades_{symbol[0]}{symbol[1]}"} 
                            }
     

                            await websocket.send(json.dumps(req))
                            self._listener.on_sent(json.dumps(req))
     
                        elif channel == Channel.book:

                            req = {
                                "event": "bts:subscribe",
                                "data":{"channel": f"diff_order_book_{symbol[0]}{symbol[1]}"} 
                            }
     
                            await websocket.send(json.dumps(req))
                            self._listener.on_sent(json.dumps(req))
                             

                # async def ping():
                #     pong_waiter = await websocket.ping('ping')
                #     self._listener.on_sent('ping')
                #     logger.info('bitstamp,send ping ..')

                #     await pong_waiter 
                #     self._listener.on_recv('pong')
                #     logger.info('bitstamp,recv pong ..')
                
                # timer = Timer(10,ping,0)


                for c in self._channels:
                    if c == Channel.book:

                        for symbol in self._symbols:
                            
                            coin = symbol[0]
                            currency = symbol[1]


                            sync_url = SYNC_BOOK_URL % f"{coin.lower()}{currency.lower()}"
                            
                            logger.info(f"bitstamp,sync order book,will call:{sync_url}")
                            
                            async with aiohttp.ClientSession() as session:
                                async with session.get(sync_url) as resp:
                                    plain = await resp.text()
                                    
                                    logger.info(f"bitstamp,sync order book,responsed")
                                    
                                    j = json.loads(plain)
                            
                                    self._listener.on_recv(plain)
                                

                                    item = j
                                    ts = float(j.get('timestamp'))

                                    converted = self.convert_book_snapshot(item)

                                    self._listener.on_resolve(coin,currency,'book/snapshot',None,ts,item)
                                    self._listener.on_book_snapshot(coin,currency,ts,converted)




                logger.info('bitstamp,start recv loop.')
                
                while True:

                    res = await websocket.recv()
                    self._listener.on_recv(res)

                    # timer.refresh()
     
                    # if res == 'pong':
                    #     logger.info('bitstamp,recv pong ....')
                    #     continue

                    line = json.loads(res)
                    event = line.get('event')




                    if 'trade' == event:

                        data = line.get('data')
                        c = line.get('channel')

                        coin = None
                        currency = None
                        channel = None

                        for chan in self._channels:
                            for symbol in self._symbols:

                                if chan == Channel.trade and c == f"live_trades_{symbol[0]}{symbol[1]}":
                                    coin = symbol[0]
                                    currency = symbol[1]
                                    channel = Channel.trade


                                    if re.match(r'live_trades_.*', c):
                                        tid = data.get('id')
                                        ts = float(data.get('microtimestamp'))/1000000
                                        current_ts = int(ts/3600)

                                        item = data
         
                                        converted = self.convert_trade(item)

                                        self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                                        self._listener.on_trade(coin,currency,ts,converted)



                    elif 'data' == event:
                        data = line.get('data')
                        c = line.get('channel')

                        coin = None
                        currency = None
                        channel = None

                        for chan in self._channels:
                            for symbol in self._symbols:

                                if chan == Channel.book and c == f"diff_order_book_{symbol[0]}{symbol[1]}":
                                    coin = symbol[0]
                                    currency = symbol[1]
                                    channel = Channel.book

                                    bids = data.get('bids')
                                    asks = data.get('asks')
                                    ts = float(data.get('timestamp'))
                                    current_ts = int(ts/3600)

                                    item = data

                                    converted = self.convert_book_update(item)
                                    
                                    self._listener.on_resolve(coin,currency,channel.value + '/update',None,ts,item)
                                    self._listener.on_book_update(coin,currency,ts,converted)




                    
                    if last_ts and current_ts and current_ts > last_ts:
                            self._listener.on_flag(last_ts*3600)

                    last_ts = current_ts   


            except websockets.ConnectionClosed as e:
                self._listener.on_end()
                    
                logger.warning(str(e))

                raise

            except Exception as e:

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





