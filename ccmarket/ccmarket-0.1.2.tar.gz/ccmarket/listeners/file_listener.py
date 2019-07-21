import os
import time
import json
import hashlib
import logging
from datetime import datetime

from ..base_listener import BaseListener

logger = logging.getLogger(__name__)


def create_dir(filename):
    
    if not os.path.exists(os.path.dirname(filename)):
        try:
            logger.debug(f'filename:{filename}')
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            raise

def record_file_path(exchange,timestamp,file_root_path):
     
    now = datetime.fromtimestamp(timestamp)
    
    filename = f"{file_root_path}/records/{exchange}/{now.year}/{now.month:02d}/{now.day:02d}/{now.hour:02d}.txt"

    return filename

def resolve_file_path(exchange,timestamp,file_root_path):
     
    now = datetime.fromtimestamp(timestamp)
    
    filename = f"{file_root_path}/resolves/{exchange}/{now.year}/{now.month:02d}/{now.day:02d}/{now.hour:02d}.txt"

    return filename

class FileListener(BaseListener):

    def __init__(self,ex,file_root_path):
        super(FileListener, self).__init__(ex)
       
        self._file_root_path = file_root_path

    def on_sent(self,plain):
        logger.debug(f"{self._exchange},send:{plain}")

        ts = time.time()

        filename = record_file_path(self._exchange,ts,self._file_root_path) 

        logger.debug(f"datafile:{filename}")
        create_dir(filename)

        with open(filename, 'a') as the_file:
            the_file.write(f"{ts},send:{plain}\n")
            logger.debug(f"{self._exchange},{ts},send:{plain}\n")

    def on_recv(self,plain):

        logger.debug(f"{self._exchange},recv:{plain}" )
        
        ts = time.time()

        filename = record_file_path(self._exchange,ts,self._file_root_path) 

        logger.debug(f"datafile:{filename}")
        create_dir(filename)

        with open(filename, 'a') as the_file:
            the_file.write(f"{ts},recv:{plain}\n")
            logger.debug(f"{self._exchange},{ts},recv:{plain}")

    def on_start(self):

        ts = time.time()

        filename = record_file_path(self._exchange,ts,self._file_root_path) 

        logger.debug(f"datafile:{filename}")
        create_dir(filename)

        with open(filename, 'a') as the_file:
            the_file.write(f"{ts},start\n")

    def on_end(self):

        ts = time.time()

        filename = record_file_path(self._exchange,ts,self._file_root_path) 

        logger.debug(f"datafile:{filename}")
        create_dir(filename)

        with open(filename, 'a') as the_file:
            the_file.write(f"{ts},end\n")

    def on_resolve(self,coin,currency,channel,cid,ts,detail):

        logger.debug(f"{self._exchange},{coin},{currency},{channel},{cid},{ts},{detail}" )

        filename = resolve_file_path(self._exchange,ts,self._file_root_path) 

        create_dir(filename)

        with open(filename, 'a') as the_file:

            if not cid:

                hash_object = hashlib.md5(json.dumps(detail).encode('utf8'))
                cid = 'md5_' + hash_object.hexdigest()

            the_file.write(f"{coin},{currency},{channel},{cid},{ts},{json.dumps(detail)}\n")

    def on_trade(self,coin,currency,ts,detail):
        pass

    def on_book_update(self,coin,currency,ts,detail):
        pass

    def on_book_snapshot(self,coin,currency,ts,detail):
        pass
