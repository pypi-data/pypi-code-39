import time
import json
import hashlib
import logging
from redis import StrictRedis

from ..common.timer import Timer
from ..base_listener import BaseListener

logger = logging.getLogger(__name__)

def update_books(books,coin,currency,asks,bids,timestamp):

    logger.debug(f"update depth,{coin}_{currency}, asks:{asks} , bids:{bids} , timestamp:{timestamp}\n")

    key = "%s_%s" % (coin,currency)

    
    if asks:
        curr_asks = books.setdefault(key,{}).setdefault('asks',[])
    
        for item in asks:

            arr = [n for n in curr_asks if n[0] != item[0]]

            if item[1] != '0':
                arr.append(item)

            curr_asks = arr

        sorted_asks = sorted(curr_asks, key=lambda a: a[0])[0:200]  # 按每个元素的第一个数据排序
        books.setdefault(key,{})['asks'] = sorted_asks

    if bids:        
        curr_bids = books.setdefault(key,{}).setdefault('bids',[])

        for item in bids: 

            arr = [n for n in curr_bids if n[0] != item[0]]

            if item[1] != '0':
                arr.append(item)

            curr_bids = arr

    
        sorted_bids = sorted(curr_bids, key=lambda a: a[0],reverse=True)[0:200]  # 按每个元素的第一个数据排序
        books.setdefault(key,{})['bids'] = sorted_bids
      
    books.setdefault(key,{})['timestamp'] = timestamp




class RedisListener(BaseListener): 
    def __init__(self,ex ,redis_host, redis_port):
        super(RedisListener, self).__init__(ex)

        self._redis = StrictRedis(host=redis_host, port=redis_port , db=0 ,decode_responses=True)

        self._books = {}

    def on_sent(self,plain):
        pass

    def on_recv(self,plain):
        pass

    def on_start(self):
        pass
    
    def on_end(self):
        pass

    def on_resolve(self,coin,currency,channel,cid,ts,detail):
        pass

    def on_flag(self,ts):

        pass
    def on_trade(self,coin,currency,ts,detail):
        key = f"{self._exchange}_{coin}_{currency}_trade"
        self._redis.lpush(key , json.dumps(detail))
        self._redis.ltrim(key, -20,-1)

    def on_book_update(self,coin,currency,ts,detail):

        symbol  = f'{coin}_{currency}'

        update_books(self._books , coin,currency , detail.get('asks'),detail.get('bids'),ts)
    
        key = f"{self._exchange}_{symbol}_book"
        self._redis.set(key, json.dumps(self._books[symbol]))
    
    def on_book_snapshot(self,coin,currency,ts,detail):
        
        symbol  = f'{coin}_{currency}'

        self._books.setdefault(symbol,{})['asks'] = detail.get('asks')
        self._books.setdefault(symbol,{})['bids'] = detail.get('bids')
        self._books.setdefault(symbol,{})['timestamp'] = ts

        key = f"{self._exchange}_{symbol}_book"
        self._redis.set(key, json.dumps(self._books[symbol]))
        
        
