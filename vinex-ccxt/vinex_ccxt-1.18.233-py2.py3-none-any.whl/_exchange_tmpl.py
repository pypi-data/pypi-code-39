# -*- coding: utf-8 -*-

from ccxt.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InvalidOrder


class qtrade (Exchange):

    def describe(self):
        return self.deep_extend(super(qtrade, self).describe(), {
            'id': 'qtrade',
            'name': 'qTrade',
            'countries': ['US'],
            'rateLimit': 500,
            # 'has': {
            #     'fetchCurrencies': True,
            #     'fetchTickers': True,
            #     'fetchOpenOrders': True,
            #     'fetchMyTrades': True,
            #     'fetchDepositAddress': True,
            # },
            'urls': {
                'logo': 'hhttps://qtrade.io/images/logo.png',
                'api': 'https://api.qtrade.io/v1',
                'www': 'https://qtrade.io/',
                'doc': 'https://qtrade-exchange.github.io/qtrade-docs/',
                'fees': 'https://qtrade.io/fees',
                'referral': 'https://qtrade.io/?ref=AZCXUQ6P5KCG',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'market/{market}',
                        'currencies',
                        'tickers',
                        'ticker/{market}',
                        # 'ticker_by_id/{market_id}',            # NOTE: dont implement
                        'orderbook/{market}',
                        # 'orderbook_by_id/{market_id}',         # NOTE: dont implement
                        'market/{market_id}/ohlcv/{interval}',
                    ],
                },
                'private': {
                    'get': [
                        # 'user/me',                             # NOTE: dont implement
                        'user/balances',
                        # 'user/market/:market_id',              # NOTE: dont implement
                        'user/orders',
                        'user/order/{order_id}',
                        'user/withdraws',
                        'user/withdraw/{withdraw_id}',
                        'user/deposits',
                        # 'user/deposit/{deposit_id}',           # NOTE: This endpoint currently non-functional
                        'user/transfers'                         # NOTE: Returns a list of the user's Transfers and metadata.
                    ],
                    'post': [
                        'user/cancel_order',
                        # 'user/deposit_address/{currency}'       # NOTE: dont implement

                        'user/sell_limit',
                        'user/buy_limit',
                    ],
                },
            },
            'commonCurrencies': {
                'EPC': 'Epacoin',
                'ABC': 'Anti Bureaucracy Coin',
            },
            'fees': {
                'trading': {
                    'maker': 0.005,
                    'taker': 0.005,
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })


# Public:
# TODO: fetch_markets()
# TODO: market()
# TODO: fetch_ticker()
# TODO: fetch_order_book()
# TODO: fetch_fees()

# Private:
# TODO: fetch_balance()
# TODO: create_order()
# TODO: cancel_order()
# TODO: fetch_order()
# TODO: fetch_open_orders()
