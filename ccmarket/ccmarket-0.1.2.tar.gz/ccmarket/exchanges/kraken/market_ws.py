#!/usr/bin/env python3

# api docs
#https://www.kraken.com/zh-cn/features/websocket-api

import asyncio
import websockets 
import json
import hashlib
import logging
                
import traceback

from ...const import Channel
from ...base_market_ws import BaseMarketWs
from .const import WS_URL, SYMBOLS

CHANNELS={
    Channel.book:'book',
    Channel.trade:'trade'
}
    

logger = logging.getLogger(__name__)


class MarketWs(BaseMarketWs):
    """docstring for OkexAdapter"""

    def __init__(self,exchange,symbols,channels,listeners):
        super(MarketWs, self).__init__(exchange,symbols,channels,listeners)
         
        self._channelIds = {}


    def convert_trade(self,origin):
        price = origin[0]
        size  = origin[1]
        side  = 'buy' if origin[3]=='b' else 'sell' 
        ts    = float(origin[2])


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

        logger.info(f"{self._exchange},book/update,{msg}")

        asks = msg.get('a')
        bids = msg.get('b')

        ts0 = 0

        lines = {}

        if asks:
            for ask in asks:
                ts = float(ask[2])
                # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
                # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()

                lines.setdefault('asks',[]).append([ask[0],ask[1]])

                if ts > ts0:
                    ts0 = ts


        if bids:
            for bid in bids:
                ts = float(bid[2])
                # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
                # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()

                lines.setdefault('bids',[]).append([bid[0],bid[1]])

                if ts > ts0:
                    ts0 = ts

        lines['ts'] = ts

        return lines

    def convert_book_snapshot(self,msg):
        
        asks = msg.get('as')
        bids = msg.get('bs')


        return {
            "asks":asks,
            "bids":bids
        }

    def run_task(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.task())

        except Exception as e:
            logger.error( 'Adapter ERROR, %s ,%s' , e, traceback.format_exc() ) 

    async def task(self):
         
         
        try:
            await self.connect()

        except Exception as e:
            
            logger.error(f"kraken,connect error,will reconnect,{e},{traceback.format_exc()}")
            
            await self.task()
 
    async def connect(self):

        logger.info(f"kraken,will connect to:{WS_URL}")
        
        async with websockets.connect(WS_URL) as websocket:

            last_ts = None
            current_ts = None

            self._listener.on_start()

            try:
                pairs = []
                for symbol in self._symbols:
                
                    pair = f"{symbol[0]}/{symbol[1]}".upper()
                    
                    pairs.append(pair)


                for channel in self._channels:
                    c = CHANNELS[channel] 
                    

                    req = {
                        "event": "subscribe",
                        "pair": pairs,
                        "subscription": {
                            "name": c
                        }
                    }
 
                    await websocket.send(json.dumps(req))
                    self._listener.on_sent(json.dumps(req))

                res = await websocket.recv()
                self._listener.on_recv(res)
 

                logger.info('kraken,start recv loop.')
                
                while True:

                    res = await websocket.recv()
                    self._listener.on_recv(res)
                    # timer.refresh()
      
                    if res == 'pong':
                        continue

                         

                    line = json.loads(res)



                    # if isinstance(line,dict) and line.get('event') == 'pong':
                    #     print('pong:' , line)

                    #     pass

                    if isinstance(line,dict) and line.get('status') == 'subscribed':
                        
                        logger.info(f"kraken,subscribed:{line}" )
                        
                        symbol = line.get('pair').lower().split('/')
                        coin = symbol[0]
                        currency = symbol[1]
                        channel = None
                        channelId = line.get('channelID')

                        for item in self._channels:
                            if CHANNELS[item] == line.get('subscription').get('name'):
                                channel = item


                        self._channelIds[str(channelId)] = {
                            'channel':channel,
                            'coin': coin,
                            'currency':currency
                        }

                        logger.info(f"kraken,channel ids:{self._channelIds}")


                        pass

                        # for subscribe in self.subscribes:
                        #     if line.get('channel') == subscribe.get('channel') and line.get('symbol') == subscribe.get('symbol') :
                        #         subscribe['chanId'] = line.get('chanId')

                    elif isinstance(line,list):
 

                        # for subscribe in self.subscribes:
                        #     if line[0] == subscribe.get('chanId'):
                        #         cb = subscribe.get('callback')

                        #         cb(line , subscribe.get('coin') , subscribe.get('currency'))


                        channelId = line[0]
                        channelMsg = line[1]

                        channelObj = self._channelIds.get(str(channelId))
                        coin = channelObj.get('coin')
                        currency = channelObj.get('currency')
                        channel = channelObj.get('channel')
 

                        # if 'ticker' == channel:
                            
                        #     ask = channelMsg[2]
                        #     bid = channelMsg[0]
                        #     last = channelMsg[6]

                        #     print(ask,bid,last)

                        #     self._listener.sync_ticker (coin,currency
                        #         ,last,ask,bid,None)

                        #     if self.test_ticker:
                        #         break

                        # elif 'book' == channel:
                        #     asks = []
                        #     bids = []


                        #     for item in channelMsg:
                        #         if item[2] > 0:
                        #             bids.append([item[0],item[2],item[1]])
                        #         else:
                        #             asks.append([item[0],-item[2],item[1]])

                        #     print('asks:' , asks, 'bids:' , bids)



                        #     self._listener.sync_book(coin,currency,asks,bids,None)

                        #     if self.test_book:
                        #         break

                        #     pass

                        if Channel.trade == channel:

                            for item in channelMsg:

                                # logger.info( line)

                                ts = float(item[2])
                                current_ts = int(ts/3600)


                                hash_object = hashlib.md5(json.dumps(item).encode('utf8'))
                                tid = 'md5_' + hash_object.hexdigest()

 
                                converted = self.convert_trade(item)

                                self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                                self._listener.on_trade(coin,currency,ts,converted)

         
                        elif Channel.book == channel:

                            ts = 0

                            asks = channelMsg.get('as')
                            bids = channelMsg.get('bs')
                            asks2 = channelMsg.get('a')
                            bids2 = channelMsg.get('b')

                            for item in [asks,bids,asks2,bids2]:
                                if item:
                                    for i in item:
                                        t = float(i[2])
                                        if ts < t:
                                            ts = t

                                            current_ts = int(ts/3600)

                            action = ''
                            if asks:
                                
                                item = channelMsg

                                converted = self.convert_book_snapshot(item)

                                self._listener.on_resolve(coin,currency,channel.value + '/snapshot',None,ts,item)
                                self._listener.on_book_snapshot(coin,currency,ts,converted)


                            else:
                                
                                item = channelMsg

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


if __name__ == '__main__':
 
    pass





