"""
test the integer field
"""

from gerridae import Item, TextField, Spider


class BaiduItem(Item):
    name = TextField(css_select='#su')


class BaiduSpider(Spider):
    start_urls = ['https://www.baidu.com']

    def parse(self, response):
        for item in BaiduItem.get_items(html=response.text):
            print(item)


def test_spider():
    BaiduSpider.start()


if __name__ == '__main__':
    test_spider()
