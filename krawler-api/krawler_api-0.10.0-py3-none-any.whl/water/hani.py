import requests

from lxml import html

base_url = 'http://www.hani.co.kr/'


def get_hrefs(limit=10):
    page = requests.get(base_url, allow_redirects=True)
    tree = html.fromstring(page.content)
    hrefs_ele = tree.xpath("//a[contains(@href,'html') and starts-with(@href,'/')]")

    hrefs = set([href.values()[0] for href in hrefs_ele])

    return [*hrefs, ][:limit]


def extract(href=None):
    url = base_url + href
    page = requests.get(url, allow_redirects=True)
    tree = html.fromstring(page.content)

    title = tree.xpath("//div[@id='article_view_headline']/h4/span[@class='title']/text()")
    subtitle = tree.xpath("//div[@class='article-text-font-size']/div[@class='subtitle']/text()")
    content = tree.xpath("//div[@class='article-text-font-size']/div[@class='text']/text()")
    register = tree.xpath("//p[@class='date-time']/span[1]/text()")

    ele = dict(
        title="".join(title),
        subtitle="".join(subtitle),
        content="".join(content),
        register="".join(register),
        url=url
    )
    return ele
