import requests
import json

class Fanslook:
    def __init__(self,page=5):
        self.__doc__ = '数据来源：biliob.com \n 网站作者：Jannchie见齐'

        self.headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36",
        }
        self.burl = 'https://www.biliob.com/api/event/fans-variation?pagesize=' + str(page)

        self.fjson = json.loads(requests.get(self.burl,headers=self.headers).text)

        self.case = self.fjson['content']
        self.fans_list = [[p["author"],p["mid"],p["variation"]] for p in self.case ]
    
    def fans(self):
        return self.fans_list

    def copyright(self):
        print('''
        数据来源：biliob.com \n 
        网站作者：Jannchie见齐 \n
        模块作者:Lixiaobai
        ''')