import asyncio
import aiohttp
from lxml import etree
import json
loop=asyncio.get_event_loop()
result=[]
def get(url,params=None,headers=None,cookies=None,proxy=None,timeout=3):
    return __request(urls=[url], method='GET', params=params, headers=headers, cookies=cookies, proxy=proxy,
                   timeout=timeout)[0]

def gets(urls,params=None,headers=None,cookies=None,proxy=None,timeout=3):
    return __request(urls=urls, method='GET', params=params, headers=headers, cookies=cookies, proxy=proxy,
                     timeout=timeout)
def post(url,params=None,headers=None,cookies=None,proxy=None,timeout=3):
    return __request(urls=[url],method='POST',params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)[0]

async def main(url,method=None,params=None,headers=None,cookies=None,proxy=None,timeout=3):
    # 创建一个session对象
    async with aiohttp.ClientSession() as sess:
        resp=await sess.request(url=url,method=method,params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout)
        result.append(await MyResponse(resp.read(),resp))

def __request(urls,method=None,params=None,headers=None,cookies=None,proxy=None,timeout=3):
    tasks=[]
    global result
    result = []
    for url in urls:
        tasks.append(main(url=url,method=method,params=params,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout))
    loop.run_until_complete(asyncio.wait(tasks))
    return result


def get_dict_from_params(str):
    p={}
    for s in str.split('\n'):
        datas=s.split(sep=':',maxsplit=1)
        p.update({datas[0].strip():datas[1].strip()})
    return p

class MyResponse(object):
    def __init__(self,body,resp):
        self.body=body
        self.resp=resp
    @property
    def text(self):
        try:
            return self.body.decode('utf-8')
        except:
            return self.body.decode('gbk')

    # key 自动抽取json中的所有符合的数据  递归

    def get_values_by_key(self,key, json):
        result = []  # 保存找到的所有value值
        # 1.判断json的类型
        if isinstance(json, dict):
            # 2.如果是字典
            # 2.1 判断key是否在字典的keys里面
            if key in json.keys():
                # 2.1.1 在  value=value 添加到result中
                result.append(json.get(key))
            else:
                # 2.1.2 不在 在字典的values中继续查找（遍历values）
                for value in json.values():
                    result += self.get_values_by_key(key, value)
        # 3. 如果是列表
        elif isinstance(json, list):
            # 3.1 遍历列表
            for j in json:
                # 3.2 在每个字典对象中继续查找key
                result += (self.get_values_by_key(key, j))
        else:
            return []
            # 4.都不是，直接返回
        return result
    @property
    def json(self):
        return json.loads(self.body)

    def get_element_from_xpath(self,str):
        nodes=etree.HTML(self.body).xpath(str)
        return nodes[0]
    def get_elements_from_xpath(self,str):
        return etree.HTML(self.body).xpath(str)

    @property
    def headers(self):
        return self.resp.headers
    @property
    def cookies(self):
        return self.resp.cookies