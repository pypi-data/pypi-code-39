from hy.core.language import first, last
import os
import sys
import requests
import json
import csv
from selectolax.parser import HTMLParser
api_allegro_search = 'https://allegro.pl/listing'


def un_pscze(s):
    polish = {'0104': 'Ą', '0106': 'Ć', '0118': 'Ę', '0141': 'Ł', '0143':
        'Ń', '00d3': 'Ó', '015a': 'Ś', '0179': 'Ź', '017b': 'Ż', '0105':
        'ą', '0107': 'ć', '0119': 'ę', '0142': 'ł', '0144': 'ń', '00f3':
        'ó', '015b': 'ś', '017a': 'ź', '017c': 'ż'}
    for k, v in polish.items():
        what = '\\u{}'.format(k)
        s = s.replace(what, v)
    return s


def get_atts(q='', link=''):
    if not link:
        lax = HTMLParser(requests.get(api_allegro_search, params={'string':
            q}).text)
        try:
            link = lax.css_first('article a').attributes['href']
        except Exception:
            link = None
        if not link:
            it = lax.css('a')
            it = list(filter(lambda a: 'href' in a.attributes and 
                'allegro.pl/oferta' in a.attributes['href'], it))
            it = it.attributes
            it = it['href']
            link = it
            _hy_anon_var_3 = None
        else:
            _hy_anon_var_3 = None
        _hy_anon_var_4 = _hy_anon_var_3
    else:
        _hy_anon_var_4 = None
    exit() if not link else None
    lax = HTMLParser(requests.get(link).text)
    res = {'search_request': q}
    for li in list(map(lambda x: x.text(), lax.css_first(
        'a[name=parameters],div.carousel-item a[href*=oferta]').parent.css(
        'li'))):
        li = li.encode('utf-8').decode('utf-8')
        res[un_pscze(first(li.split(':', 1)))] = un_pscze(last(li.split(':',
            1)))
    res['query'] = q
    return res

