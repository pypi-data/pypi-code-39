from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent

def get_ip():
    try:
        ua = UserAgent()
    except:
        ua = UserAgent()
    baseurl = 'https://www.kuaidaili.com/free/inha/'
    ip_list = []
    for i in range(1,11):
        headers = {
            'User-Agent': ua.random
        }
        url = baseurl + str(i)
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ipbody = soup.find_all('tbody')[0]
        ips = ipbody.find_all('tr')

        for ip in ips:
            infos = ip.text.split('\n')
            host = infos[1]
            port = infos[2]
            ip_list.append('http://'+host+':'+port)
        time.sleep(2)
    text = '\n'.join(ip_list)
    f = open('ip.txt', 'w')
    f.write(text)
    f.close()

if __name__ == '__main__':
    get_ip()





