# -*- coding: utf-8 -*-

"""
基于HTTP的下载器
"""

import aiohttp
import requests

from contextlib import closing
from middleware.utils.file_util import FileUtil


async def post(url, params):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=params) as resp:
                return await resp.json()
        except aiohttp.client_exceptions.ClientConnectorError:
            result = {"status": 205}
        except aiohttp.client_exceptions.InvalidURL:
            result = {"status": 206}
        except aiohttp.client_exceptions.ServerTimeoutError:
            result = {"status": 207}
        except aiohttp.client_exceptions.ServerDisconnectedError:
            result = {"status": 208}
        return result


async def post_file(url, params, file_path):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=FileUtil.file_upload_sender(file_path=file_path), params=params) as resp:
                result = await resp.json()
        except aiohttp.client_exceptions.ClientConnectorError:
            result = {"status": 205}
        except aiohttp.client_exceptions.InvalidURL:
            result = {"status": 206}
        except aiohttp.client_exceptions.ServerTimeoutError:
            result = {"status": 207}
        except aiohttp.client_exceptions.ServerDisconnectedError:
            result = {"status": 208}
    return result


async def download_file(url, params, local_path):
    with closing(requests.get(url, params=params, stream=True, timeout=3600)) as response:
        chunk_size = 4096  # 单次请求最大值
        content_size = int(response.headers['content-size'])  # 内容体总大小
        data_count = 0
        with open(local_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, local_path), end='')
        print('')
