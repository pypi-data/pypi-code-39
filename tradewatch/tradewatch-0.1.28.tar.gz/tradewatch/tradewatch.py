import hy.macros
from hy.core.shadow import hyx_Xplus_signX
from anarcute import *
hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')
import requests
import json
import datetime


class TradeWatch(object):

    def __init__(self, auth):
        self.auth = auth
        self.api_tx = 'https://tradewatch.pl/api/tx/list'
        self.api_atts = 'https://tradewatch.pl/api/util/get-atts'
        return None

    def get_stat(self):
        return requests.get('https://tradewatch.pl/api/account/request-stats',
            params={'auth': self.auth}).json()

    def get_tx_by_eans(self, eans, date_from='2016-01-01', date_to=None):
        MAX_TX = 100
        if MAX_TX < len(eans):
            _hy_anon_var_5 = +[*apply_to_chunks(self.get_tx_by_eans, atts,
                MAX_TX)]
        else:
            if not type(eans) in (list, tuple):
                eans = [eans]
                _hy_anon_var_3 = None
            else:
                _hy_anon_var_3 = None
            if not date_to:
                date_to = (datetime.timedelta(days=1) + datetime.datetime.now()
                    ).strftime('%Y-%m-%d')
                _hy_anon_var_4 = None
            else:
                _hy_anon_var_4 = None
            _hy_anon_var_5 = requests.get(self.api_tx, params={'auth': self
                .auth, 'product-eans': ','.join((lambda arr: list(map(str,
                arr)))(eans)), 'date-from': date_from, 'date-to': date_to}
                ).json()
        return _hy_anon_var_5

    def get_tx(*args, **kwargs):
        return self.get_tx_by_eans(*args, **kwargs)

    def get_atts(self, atts):
        MAX_ATTS = 500
        return hyx_Xplus_signX([], *apply_to_chunks(self.get_atts, atts,
            MAX_ATTS)) if MAX_ATTS < len(atts) else requests.get(self.
            api_atts, params={'auth': self.auth, 'ids': ','.join((lambda
            arr: list(map(str, arr)))(atts))}).json()

