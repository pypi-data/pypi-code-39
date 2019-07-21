#!/usr/bin/env python3

# https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md

import aiohttp
import websockets 
import json
import logging

from datetime import datetime,timezone

from ...const import Channel

from ...base_market_ws import BaseMarketWs
from .const import WS_URL, SYMBOLS,SYNC_BOOK_URL

logger = logging.getLogger(__name__)


CHANNELS ={
    Channel.book:'depth',
    Channel.trade:'trade'
}


class MarketWs(BaseMarketWs):
    """ Binance Market Websocket Sdk 
    Args:
        channels:ticker|depth|trade

    """

    def __init__(self,exchange ,symbols ,channels,listeners):

        super(MarketWs, self).__init__(exchange,symbols,channels,listeners)
        
        self._channelIds = {}
        self.book_cache = {}

    def convert_trade(self,origin):

        # print('origin,' , origin)

        price = origin.get('p')
        size  = origin.get('q')
        side  = 'sell' if origin.get('m') else 'buy'  
        ts    = origin.get('E')/1000

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
        
        first_update_id = msg.get('U')
        last_update_id = msg.get('u')
        bids = msg.get('b')
        asks = msg.get('a')
        ts = msg.get('E')/1000

        # ts = datetime.fromtimestamp(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()

        # lines = []

        # for bid in bids:
        #     lines.append([str(ts),str(bid[0]),str(bid[1]),'bid'])

        # for ask in asks:
        #     lines.append([str(ts),str(ask[0]),str(ask[1]),'ask'])

        return {
            "asks":asks,
            "bids":bids,
            "ts":ts,
            "cid":first_update_id
        }

    def convert_book_snapshot(self,msg):

        last_update_id = msg.get('lastUpdateId')
        asks = msg.get('asks')
        bids = msg.get('bids')

        return {
            "asks":asks,
            "bids":bids
        }


    async def connect(self):    

        flag = True
        snapshot = None
        ucids    = []

        # binance 通过定制websocket url的参数来实现订阅
        streams = []

        for channel in self._channels:
            c = CHANNELS[channel]
            
            for symbol in self._symbols:
                s = f"{symbol[0]}{symbol[1]}"

                stream_name = f"{s}@{c}"
                streams.append(stream_name)

        url = f"{WS_URL}/stream?streams={'/'.join(streams) }"

        logger.info(f"binance,will connect to: {url}" )

        async with websockets.connect(url) as websocket:


            last_ts = None
            current_ts = None

            self._listener.on_start()

            try:

                for c in self._channels:
                    if c == Channel.book:

                        for symbol in self._symbols:
                            
                            coin = symbol[0]
                            currency = symbol[1]


                            sync_url = SYNC_BOOK_URL % f"{coin.upper()}{currency.upper()}"
                            
                            logger.info(f"binance,sync order book,will call:{sync_url}")
                            
                            async with aiohttp.ClientSession() as session:
                                async with session.get(sync_url) as resp:
                                    plain = await resp.text()
                                    
                                    logger.info(f"binance,sync order book,responsed")
                                    
                                    j = json.loads(plain)
                            
                                    self._listener.on_recv(j)

                                    snapshot = [coin,currency,'book/snapshot',j.get('lastUpdateId'),None,j]
                                    for ucid in ucids:
                                        if j.get('lastUpdateId') <= ucid[0]:

                                            item = j
                                            ts = ucid[1]-0.000001

                                            converted = self.convert_book_snapshot(item)

                                            self._listener.on_resolve(coin,currency,  'book/snapshot',j.get('lastUpdateId'),ts,item)
                                            self._listener.on_book_snapshot(coin,currency,ts,converted)




                                            flag = False 

                logger.info('binance,start recv loop.')
                
                while True:

                    res = await websocket.recv()
                    
                    self._listener.on_recv(res)
                    
                    # if res == 'ping':
                    #     await websocket.send('pong')
                    #     self._listener.on_sent('pong')
                    #     logger.info('binance,recv ping ..')
                        
                    #     continue


                    line = json.loads(res)

                    stream = line.get('stream')
                    data = line.get('data')
                    items = stream.split('@')



                    coin = None
                    currency = None
                    channel = None

                    for symbol in self._symbols:
                        if f"{symbol[0]}{symbol[1]}" == items[0]:

                            coin = symbol[0]
                            currency = symbol[1]

                    for c in self._channels:
                        if CHANNELS[c ] == items[1]:
                            channel = c


                    if Channel.trade == channel:
                        
                        tid = data.get('t')
                        ts  = data.get('E')/1000
                        current_ts = int(ts/3600)

                        item = data

                        converted = self.convert_trade(item)

                        self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                        self._listener.on_trade(coin,currency,ts,converted)


                    elif Channel.book == channel:
                        
                        cid = data.get('u')

                        ts = data.get('E')/1000
                        current_ts = int(ts/3600)

                        if flag:
                            if snapshot:
                                if snapshot[3] <=  cid:
                                    self._listener.on_resolve(snapshot[0],snapshot[1],snapshot[2],snapshot[3],ts-0.000001,snapshot[5])
                                    flag = False
                            else:
                                ucids.append([cid,ts])

                        item = data

                        converted = self.convert_book_update(item)
                        
                        self._listener.on_resolve(coin,currency,channel.value + '/update',cid,ts,item)
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





