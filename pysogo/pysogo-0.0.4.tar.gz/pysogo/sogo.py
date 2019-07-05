#! /usr/bin/env/python
# -*- coding:UTF-8 -*-
# import os
# import sys
# dir = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
# sys.path.append(dir)
# import pybrowser


import pysogo as pybrowser
import time
import logging



# Default sogo selector



class SogoEngine(object):

    def __init__(self):
        self.default_sogo_headers = None
        self.url_home = "https://%(tpe)s.sogou.com/%(tpe)s?query=%(query)s&type=2&ie=utf8&page=%(page)s"
        self.selectorLinks = '#main > div.news-box > ul > li'
        self.selectorTimestring = 'span.s2'

    # Return a Generator that yield URLs, using the given query string.
    def search(self, query, pause=2.0, user_agent=None, tpe='', num=10, start=1,
               end=None, tbs='', only_current_page=False, allow_domains=None, deny_domains=None,
               selector_links=None, attrs=None):
        """

        :param str query: Query String. Must not be URLencode
        :param float pause: A Lapse to wait between HTTP Request.
            A long Lapse can cause the search slow. A short Lapse will make the Sogo to block
            your IPs.
        :param str user_agent: Use the Default USER-AGENT for None.
        :param str tpe: Search Type (i.e web, weixin, news, videos, zhihu, pics->images ...)
        :param int num: Number of result per page
        :param int start: Offset of the first result to retrieve
        :param int/None end: Last of result to retrieve.
            Keep searching forever if None
        :param str tbs: Time limits
            (i.e d:1 last 1 day, d:2 last 2 days,
                m:1 last 1 month, y:1 last 1 year,
                '' No Time Limit)
        :param bool only_current_page: Use True to prove searching in this page /
            and Not Request next page.
        :param tuple allow_domains: Allow domains.
        :param tuple deny_domains: Deny domains.
        :return: A generator that yields URLs.
        """
        if not isinstance(pause, int) or pause < 0:
            logging.warning("`pause` should be integer and greater than 0")


        # url-encode given query string
        query = pybrowser.quote_plus(query)

        url = self.url_home % {'query':query, 'tpe':tpe, 'page':start}
        soup = self.get_soup(url, user_agent)
        selector_links = selector_links or self.selectorLinks
        links = soup.select(selector_links)

        # 计数链接条数
        count = 0
        for link in links:
            if count > num:
                break


            if attrs :
                yield link.select(attrs)
            else:
                yield link
            count += 1

        while not only_current_page and count < num :
            if pause > 0:
                time.sleep(pause)
            start += 1
            if isinstance(end, int):
                if start > end:
                    logging.error("max page is %d, but current page is %d. exit program!" %(end, start))
                    break


            url = self.url_home % {'query':query, 'tpe':tpe, 'page':start}
            soup = self.get_soup(url, user_agent)
            links = soup.select(selector_links)
            # 如果没有匹配到任何结果，则退出循环
            if len(links) == 0:
                logging.info("completed %d links from %s" % (count, tpe))
                break

            for link in links:
                if count > num:
                    break

                if attrs :
                    yield link.select(attrs)
                else:
                    yield link
                count += 1

        logging.info("completed %d/%d links!" %(count, num))


    def get_soup(self, url, user_agent):
        response = pybrowser.get_page(url=url,
                                      user_agent=user_agent,
                                      Cookie='SUV={};'.format("F"*32))
        soup = pybrowser.BeautifulSoup(response, features="lxml")
        return soup

    def search_weixin(self, query, pause=2.0, user_agent=None, num=10, start=1,
                     end=None, only_current_page=False, selector_links=None, attrs=None):
        return self.search(query=query, pause=pause, user_agent=user_agent, num=num, tpe="weixin",
                           start=start, end=end, only_current_page=only_current_page, selector_links=selector_links,
                           attrs=attrs)

    def search_zhihu(self, query, pause=2.0, user_agent=None, num=10, start=1,
                     end=None, only_current_page=False, selector_links=None, attrs=None):
        return self.search(query=query, pause=pause, user_agent=user_agent, num=num, tpe="zhihu",
                           start=start, end=end, only_current_page=only_current_page, selector_links=selector_links,
                           attrs=attrs)




if __name__ == '__main__':
    p =SogoEngine()
    for i in p.search(query='it may', tpe='weixin',
                      pause=-1,
                      num=100, start=1, end=3):
        print(i)

