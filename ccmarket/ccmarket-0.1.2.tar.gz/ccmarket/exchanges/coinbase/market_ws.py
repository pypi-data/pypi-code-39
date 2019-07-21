#!/usr/bin/env python3

'''
api docs
https://docs.pro.coinbase.com/#channels
'''

import websockets 
import json
import iso8601

import logging
                
from ...const import Channel
from ...base_market_ws import BaseMarketWs

from .const import WS_URL,SYMBOLS 

# class Channel(Enum):
#     ticker= 'ticker'
#     book  = 'level2'
#     deals = 'ticker'
    

logger = logging.getLogger(__name__)


class MarketWs(BaseMarketWs):
    """docstring for OkexAdapter"""

    def __init__(self,exchange,symbols ,channels,listeners):
        super(MarketWs, self).__init__(exchange,symbols,channels,listeners)
        
        self._channelIds = {}


    def convert_trade(self,origin):
        price = origin.get('price')
        size  = '1'
        side  = origin.get('side') or 'buy' 
        ts    = origin.get('time')


        # ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')
        # ts = iso8601.parse_date(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()
        ts = iso8601.parse_date(ts).timestamp()

        # ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%SZ')


        return {
            'price':price,
            'size':size,
            'side':side,
            'ts':ts 
        }


    def convert_book_update(self,msg):
        changes = msg.get('changes')
        ts      = msg.get('time')

        # ts = iso8601.parse_date(ts).astimezone(pytz.timezone("Asia/Shanghai")).isoformat()
        ts = iso8601.parse_date(ts).timestamp()
        
        asks = []
        bids = []
        for item in changes:
            if item[0] == 'buy':
                bids.append([str(ts), str(item[1]),str(item[2]) ])
            elif item[0] == 'sell':
                asks.append([str(ts), str(item[1]),str(item[2]) ])

        return {
            "asks":asks,
            "bids":bids,
            "ts":ts
        }

    def convert_book_snapshot(self,msg):

        asks = msg.get('asks')
        bids = msg.get('bids')

        return {
            "asks":asks,
            "bids":bids
        }

    async def connect(self ):

        ss = []
        for symbol in self._symbols:
            
            s = f"{symbol[0].upper()}-{symbol[1].upper()}"
            ss.append(s)

        cs = []
        for c in self._channels: 
            cs.append(c.value)

        cs = list(set(cs))

        cs = [
            "level2",
            "heartbeat",
            {
                "name": "ticker",
                "product_ids": ss
            }
        ]


        req = {
            "type": "subscribe",
            "product_ids": ss,
            "channels": cs
        }

        # req = {
        #     "type": "subscribe",
        #     "product_ids": [
        #         "ETH-USD",
        #         "ETH-EUR"
        #     ],
        #     "channels": [
        #         "level2",
        #         "heartbeat",
        #         {
        #             "name": "ticker",
        #             "product_ids": [
        #                 "ETH-BTC",
        #                 "ETH-USD"
        #             ]
        #         }
        #     ]
        # }

        logger.info(f"coinbase,will connect to:{WS_URL}")

        async with websockets.connect(WS_URL) as websocket:
            
            last_ts = None
            current_ts = None

            snapshots = {}

            self._listener.on_start()

            
            try:

                await websocket.send(json.dumps(req))
                self._listener.on_sent(json.dumps(req))
 
                logger.info('coinbase,start recv loop.')

                while True:

                    plain = await websocket.recv()
                    
                    self._listener.on_recv( plain )

                    # timer.refresh()
     
                    logger.debug("recv:%s", plain)

                    if plain == 'pong':
                        logger.info('coinbase,recv pong ..')
                        
                        continue

                    line = json.loads(plain)
                    

  
                    if 'ticker' == line.get('type'):

                        channel = Channel.trade
                        coin = None
                        currency = None

                        for symbol in self._symbols:
                            if f"{symbol[0].upper()}-{symbol[1].upper()}" == line.get('product_id'):

                                coin = symbol[0]
                                currency = symbol[1]

                        tid = line.get('trade_id')
                        ts = line.get('time')

                        if ts :

                            # ts = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
                            ts = iso8601.parse_date(ts).timestamp()
                            current_ts = int(ts/3600)

                            item = line

                            converted = self.convert_trade(item)

                            self._listener.on_resolve(coin,currency,channel.value,tid,ts,item)
                            self._listener.on_trade(coin,currency,ts,converted)


                    if 'snapshot' == line.get('type') :

                        channel = Channel.book

                        for symbol in self._symbols:
                            if f"{symbol[0].upper()}-{symbol[1].upper()}" == line.get('product_id'):

                                coin = symbol[0]
                                currency = symbol[1]


                        bids = line.get('bids')
                        asks = line.get('asks')

                        snapshots[f"{coin}_{currency}"] = {
                            "bids":bids,
                            "asks":asks
                        }

                    elif 'l2update' == line.get('type'):
                        
                        channel = Channel.book

                        for symbol in self._symbols:
                            if f"{symbol[0].upper()}-{symbol[1].upper()}" == line.get('product_id'):

                                coin = symbol[0]
                                currency = symbol[1]


                        ts = line.get('time')
                        # ts = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
                        ts = iso8601.parse_date(ts).timestamp()
                        current_ts = int(ts/3600)

                        ss = snapshots.get(f"{coin}_{currency}")
                        if ss:

                            item = ss
                            ts = ts-0.000001

                            converted = self.convert_book_snapshot(item)

                            self._listener.on_resolve(coin,currency,channel.value + '/snapshot',None,ts,item)
                            self._listener.on_book_snapshot(coin,currency,ts,converted)



                            del snapshots[f"{coin}_{currency}"]

                        else:
                            item = line

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





