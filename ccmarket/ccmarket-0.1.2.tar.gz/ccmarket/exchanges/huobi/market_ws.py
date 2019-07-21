#!/usr/bin/env python3

# api docs
# https://github.com/huobiapi/API_Docs/wiki/WS_request

import websockets 
import json
import gzip
import re
from datetime import datetime

import logging

from ...const import Channel
from ...base_market_ws import BaseMarketWs
from .const import WS_URL,SYMBOLS


# class Channel(Enum):
#     depth='depth'
#     trade='trade'
    

logger = logging.getLogger(__name__)


class MarketWs(BaseMarketWs):
    """docstring for OkexAdapter"""

    def __init__(self,exchange,symbols ,channels,listeners ):
        super(MarketWs, self).__init__(exchange,symbols,channels,listeners)
        
        self._channelIds = {}

        self._last_book = None

    def convert_trade(self,origin):
        price = origin.get('price')
        size  = origin.get('amount')
        side  = origin.get('direction') 
        ts    = origin.get('ts')/1000

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
        tick = msg.get('tick')
        bids = tick.get('bids')
        asks = tick.get('asks')
        ts   = tick.get('ts')/1000

        # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
        # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()
        # lines = []

        # for ask in asks:

        #     lines.append([str(ts),str(ask[0]),str(ask[1]),'ask'])
        # for bid in bids:

        #     lines.append([str(ts),str(bid[0]),str(bid[1]),'bid'])


        return {
            "asks":asks,
            "bids":bids,
            "ts":ts
        }

    def convert_book_snapshot(self,msg):
        tick = msg.get('tick')
        bids = tick.get('bids')
        asks = tick.get('asks')
        ts   = tick.get('ts')/1000

        ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
        lines = []
 

        return {
            "asks":asks,
            "bids":bids
        }
 
    async def connect(self):

        logger.info(f"huobi,will connect to:{WS_URL}")
        
        async with websockets.connect(WS_URL) as websocket:
            
            last_ts = None
            current_ts = None

            self._listener.on_start()
     
            try:

                for channel in self._channels:
                    # c = CHANNELS.get(channel)
                    for symbol in self._symbols:
                    
                        s = f"{symbol[0]}{symbol[1]}"

                        if channel == Channel.trade:

                            topic = f"market.{s}.trade.detail"

                            req = {
                                'sub': topic
                            }
                            
                            
                            await websocket.send(json.dumps(req) )
                            self._listener.on_sent(json.dumps(req))
                        elif channel == Channel.book:

                            topic = f"market.{s}.depth.step0"


                            req = {
                                'sub': topic
                            }
                            
                            
                            await websocket.send(json.dumps(req) )
                            self._listener.on_sent(json.dumps(req))

                
                logger.info('huobi,start recv loop.')
                
                while True:

                    res = await websocket.recv()
                    plain = gzip.decompress(res)
                    self._listener.on_recv(plain)


                    j = json.loads(plain)

                    # 处理ping，pong
                    pingid = j.get('ping')
                    pongid = j.get('pong')
                    if pingid:
                        j_send = {'pong':pingid}
                        p_send = json.dumps(j_send)
                        await websocket.send(p_send)
                        self._listener.on_sent(p_send)

                        # logger.info('huobi,recv ping ..')
                        # logger.info('huobi,sent pong ..')
                    if pongid:
                        logger.info('huobi,recv pong ..')



                    # timer.refresh()
     
                    
                    # if plain == 'pong':
                    #     continue

                    line = json.loads(plain)

                    if isinstance(line,dict) and line.get('ch'):

                        ch = line.get('ch')


                        coin = None
                        currency = None
                        channel = None

                        for symbol in self._symbols:
                            for item in self._channels:

                                # c = CHANNELS.get(item)
                                s = f"{symbol[0]}{symbol[1]}"

                                if item == Channel.trade:
                                    topic = f"market.{s}.trade.detail"

                                    if topic == ch:
                                
                                        coin = symbol[0]
                                        currency = symbol[1]
                                        channel = item
                                elif item == Channel.book:
                                    topic = f"market.{s}.depth.step0"

                                    if topic == ch:
                                
                                        coin = symbol[0]
                                        currency = symbol[1]
                                        channel = item

                        if re.match(r'market\..*\.trade\.detail',ch):
                            data = line.get('tick').get('data')    

                            for item in data:
                                tid = item.get('id')
                                ts = item.get('ts')/1000
                                current_ts = int(ts/3600)

                                converted = self.convert_trade(item)

                                self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                                self._listener.on_trade(coin,currency,ts,converted)

                        elif re.match(r'market\..*\.depth\.step0',ch):
                            
                            data = line.get('tick')

                            if self._last_book != None:

                                ts = data.get('ts')/1000
                                current_ts = int(ts/3600)


                                bids = data.get('bids')
                                asks = data.get('asks')

                                ubids = []
                                uasks = [] 

                                for bid in bids:
                                    if bid not in self._last_book['bids']:
                                        ubids.append(bid)
                                for ask in asks:
                                    if ask not in self._last_book['asks']:
                                        uasks.append(ask)


                                umsg = json.loads(json.dumps(line))
                                umsg['tick']['bids'] = ubids
                                umsg['tick']['asks'] = uasks

                                item = umsg

                                converted = self.convert_book_update(item)
                                
                                self._listener.on_resolve(coin,currency,channel.value + '/update',None,ts,item)
                                self._listener.on_book_update(coin,currency,ts,converted)





                            else:
                                ts = data.get('ts')/1000
                                current_ts = int(ts/3600)

                                item = line

                                converted = self.convert_book_snapshot(item)

                                self._listener.on_resolve(coin,currency,channel.value + '/snapshot',None,ts,item)
                                self._listener.on_book_snapshot(coin,currency,ts,converted)



                            self._last_book = data
                    
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





