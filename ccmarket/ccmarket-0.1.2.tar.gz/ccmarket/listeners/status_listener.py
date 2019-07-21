import time
import json
import hashlib
import logging

from ..common.timer import Timer
from ..base_listener import BaseListener

logger = logging.getLogger(__name__)


class StatusListener(BaseListener):
    
    def __init__(self,ex , connect_status_minutes):
        super(StatusListener, self).__init__(ex)
       

        # 连接状态信息
        self._connect_establish_ts = None 
        self._connect_receive_count = 0
        self._connect_status_minutes = connect_status_minutes

        timer = Timer.interval(self.run_status,0,60*self._connect_status_minutes)

    def run_status(self):

        if self._connect_establish_ts:

            run_time = time.time() - self._connect_establish_ts
            day  = int(run_time/86400)
            hour = int(run_time%86400/3600)
            minute = int(run_time%3600/60) 
            second = int(run_time%60)

            logger.info(f"{self._exchange}, 连接维持时间:{day}天{hour}时{minute}分{second}秒, 收到消息数量:{self._connect_receive_count} ")

    def on_sent(self,plain):
        pass

    def on_recv(self,plain):

        self._connect_receive_count += 1

    def on_start(self):

        logger.info(f"{self._exchange},connected" )

        self._connect_establish_ts = time.time() 
        self._connect_receive_count = 0


    def on_end(self):

        logger.info(f"{self._exchange},disconnect")

        self._connect_establish_ts = None 
        self._connect_receive_count = 0

    def on_resolve(self,coin,currency,channel,cid,ts,detail):

        pass

    def on_flag(self,ts):

        pass
        
    def on_trade(self,coin,currency,ts,detail):
        pass

    def on_book_update(self,coin,currency,ts,detail):
        pass

    def on_book_snapshot(self,coin,currency,ts,detail):
        pass