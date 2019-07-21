from enum import Enum

VERSION = '0.1.2'

#['binance','bitfinex','bitstamp','coinbase','huobi','kraken','okex']
SUPPORTED_EXCHANGES = ['binance','bitfinex','bitstamp','coinbase','huobi','kraken','okex']

class Channel(Enum):

    trade = 'trade'
    book  = 'book'

    def rlsv(value):
        if value == Channel.trade.value:
            return Channel.trade
        elif value == Channel.book.value:

            return Channel.book
        else:
            raise ValueError