
import asyncio
import logging
from typing import Optional, Union

import aiohttp

from .exceptions import TimeoutError

__all__ = ['Chrome']

class Chrome(object):

    _url= ''
    _host='localhost'
    _port=9222
    _log: Union[logging.Logger]=None

    def __init__(self, host: Optional['str']="localhost", port: Optional['int']=9222) -> None:
        self._host = host
        self._port = port
        self._url = "http://%s:%d" %(self._host, self._port)
        self._log = logging.getLogger('chromemin.Chrome')
    
    async def create_tab(self, timeout: Optional['int'] = 5*60) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url + '/json/new', timeout=timeout) as resp:
                    data = await resp.json()
            return data
        except asyncio.TimeoutError:
            msg = 'Created Tab for timeout'
            self._log.error(msg)
            raise TimeoutError(msg)
    
    async def list_tabs(self, timeout: Optional['int'] = 5*60) -> list:
        list_tab = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url + '/json', timeout=timeout) as resp:
                    data = await resp.json()
                    for tab in data:
                        if tab['type'] == 'page':
                            list_tab.append(tab)
            return list_tab
        except asyncio.TimeoutError:
            msg = 'Get Tabs for timeout'
            self._log.error(msg)
            raise TimeoutError(msg)
    
    async def activate_tab(self, tab_id: Union['str'], timeout: Optional['int'] = 5*60) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url +'/json/activate/' + tab_id, timeout=timeout) as resp:
                    return await resp.text()
        except asyncio.TimeoutError:
            msg = 'Activeate Tab for timeout in id = %s' %(tab_id)
            self._log.error(msg)
            raise TimeoutError(msg)
    
    async def close_tab(self, tab_id :Union['str'] = None, timeout: Optional['int'] = 5*60) ->(str, bool):
        try:
            if tab_id:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self._url + '/json/close/' + tab_id, timout=timeout) as resp:
                        return await resp.text()
            else:
                list_tabs = await self.list_tabs()
                async with aiohttp.ClientSession() as session:
                    for tab in list_tabs:
                        async with session.get(self._url + '/json/close/' + tab['id']) as resp:
                            pass
                return True              
        except asyncio.TimeoutError:
            if tab_id:
                msg = 'Close Tab for timeout in id = %s' %(tab_id)
            else:
                msg = 'Close All Tab for timeout'
            self._log.error(msg)
            raise TimeoutError(msg)
    
    async def version(self, timeout: Optional['int'] = 5*60)-> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._url + '/json/version', timeout=timeout) as resp:
                    return await resp.json()
        except asyncio.TimeoutError:
            msg = 'Chrome Version for timeout'
            self._log.error(msg)
            raise TimeoutError(msg)
    

