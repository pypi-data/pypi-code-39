import requests

from lxml import html

base_url = 'http://www.chosun.com/'


def get_hrefs(limit=10):
    page = requests.get(base_url, allow_redirects=True)
    tree = html.fromstring(page.content)
    hrefs_ele = tree.xpath("//dl/dt/a")

    hrefs = set([href.values()[0] for href in hrefs_ele])

    return [*hrefs, ][:limit]


def extract(href=None):
    url = href
    page = requests.get(url, allow_redirects=True)
    tree = html.fromstring(page.content)

    title = tree.xpath("//h1[@id='news_title_text_id']/text()")
    content = tree.xpath("//div[@id='news_body_id']/div[@class='par']/text()")
    register = tree.xpath("//div[@id='news_body_id']/div[@class='news_date']/text()")

    ele = dict(
        title="".join(title),
        content="".join(content),
        register="".join(register),
        url=url
    )
    return ele
