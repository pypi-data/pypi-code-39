import logging
import logging.config
import sys

linux_logging_path = sys.prefix + '/etc/ccmarket/logging.ini'
linux_config_path  = sys.prefix + '/etc/ccmarket/config.ini'

local_logging_path = './logging.dev.ini'
local_config_path = './config.ini'


def main(config_path,logging_path):

    import os

    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logging.config.fileConfig(logging_path)

    print('loggingconfig',logging.config)

    import importlib
    import asyncio
    import time
    import os
    import re
    from datetime import datetime


    from .common.timer import Timer
    from .const import SUPPORTED_EXCHANGES,Channel
    from .base_listener import BaseListener 
    from .market_ws_listener import MarketWsListener
    from .listeners.file_listener import FileListener
    from .listeners.status_listener import StatusListener
    from .listeners.redis_listener import RedisListener

    from .config import Config


    logger = logging.getLogger(__name__)


    config = Config()
    config.read(config_path)


    ex_symbols  = {}
    ex_channels = {}
    ex_market_ws_class = {}

    for ex in SUPPORTED_EXCHANGES :
        if not config.resolved[ex]['switch']:
            continue

        ex_symbols[ex]  = config.resolved[ex]['symbols']
        ex_channels[ex] = config.resolved[ex]['channels'] 

        # 加载各交易所的MarketWs类（MarketWsSdk）
        market_ws_str = f".exchanges.{ex}.market_ws"
        logger.debug(f"market_ws_str:{ market_ws_str}")
        market_ws_m = importlib.import_module(market_ws_str,__package__) 
        market_ws_class = getattr (market_ws_m, 'MarketWs')
        ex_market_ws_class[ex] = market_ws_class

    logger.info(f"read config,ex_symbols:{ex_symbols},ex_channels:{ex_channels}")
 
    loop = asyncio.get_event_loop()  
    for k,v in ex_market_ws_class.items():

        listeners = []
        if config.resolved['status_listener']['switch']:
            listeners.append(StatusListener(k,config.resolved['status_listener']['connect_status_minutes']))
        if config.resolved['file_listener']['switch']:
            listeners.append(FileListener(k,config.resolved['file_listener']['file_root_path']))
        if config.resolved['redis_listener']['switch']:
            listeners.append(RedisListener(k,config.resolved['redis_listener']['redis_host'],config.resolved['redis_listener']['redis_port']))



        market_ws = v(k,ex_symbols[k],ex_channels[k],MarketWsListener(k,listeners))
        
        logger.info(f"{k},will add task to asyncio")

        loop.create_task(market_ws.task())

    loop.run_forever()


def linux():
    
    main(linux_config_path,linux_logging_path)

if __name__ == '__main__':

    main(local_config_path,local_logging_path)