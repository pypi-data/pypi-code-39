import requests , json,logging 

from .sdk import spot_api  as spot

from ...fail_exception import FailException 
from .code_converter import rest_code
from .sdk.exceptions import OkexAPIException

logger = logging.getLogger(__name__)

class TradeRest(object):


    """docstring for CommandAdapter"""
    def __init__(self, secrets):
        super(TradeRest, self).__init__()
        self.apikey =  secrets.get('apikey')
        self.secretkey = secrets.get('secretkey')
        self.passphrase = secrets.get('passphrase')

        self.spotApi = spot.SpotAPI(self.apikey, self.secretkey, self.passphrase, True)

    def order_info(self,orderid,coin,currency):

        instrument_id = '%s-%s' % (coin,currency)
        try:
            result = self.spotApi.get_order_info(orderid , instrument_id )

            logger.debug('order_detail, resp : %s' , result )

            ret = {
                'order_id':result.get('order_id'),
                'filled_amount':result.get('filled_size'),
                'filled_volume':result.get('filled_notional'),
                'created_at':result.get('created_at'),
                'timestamp':result.get('timestamp'),
                'status':result.get('status')
            }


            if result.get('type') == 'limit' and result.get('side') == 'buy':
                ret['type'] = 'limit_buy'
                ret['price'] = result.get('price')
                ret['amount'] = result.get('size')
            elif result.get('type') == 'limit' and result.get('side') == 'sell':

                ret['type'] = 'limit_sell'
                ret['price'] = result.get('price')
                ret['amount'] = result.get('size')

            elif result.get('type') == 'market' and result.get('side') == 'buy':
                ret['type'] = 'market_buy'
                ret['volume'] = result.get('notional')

            elif result.get('type') == 'market' and result.get('side') == 'sell':
                ret['type'] = 'market_buy'
                ret['amount'] = result.get('size')

            return ret

        except OkexAPIException as e:

            logger.error('OkexAPIException:%s, %s',e.status_code,e.response.text)

            obj = e.response.json()

            code = rest_code(obj.get('code') , 40500)

            raise FailException(code,obj.get('message'))


    def limit_buy(self, price ,amount , coin , currency ):
         
        otype = 'limit'
        side = 'buy'
        instrument_id = '%s-%s' % (coin,currency)
        size = '%s' % amount  
        price = '%s' % price 
        
        logger.debug(f'otype:{otype} , side:{side} , instrument_id:{instrument_id} , price:{price} , size:{size}')

        try:
            result = self.spotApi.take_order(otype,side,instrument_id,size=size,price=price)
        
            logger.debug('limit_buy, resp : %s' , result )

            return result.get('order_id')

        except OkexAPIException as e:
            logger.error('OkexAPIException:%s, %s',e.status_code,e.response.text)

            obj = e.response.json()

            code = rest_code(obj.get('code'))

            raise FailException(code,obj.get('message'))

        
    def limit_sell(self, price ,amount , coin , currency ):
         
        otype = 'limit'
        side = 'sell'
        instrument_id = '%s-%s' % (coin,currency)
        size = '%s' % amount  
        price = '%s' % price 
        
        try:
            result = self.spotApi.take_order(otype,side,instrument_id,size=size,price=price)
            logger.debug('limit_sell, resp : %s' , result )

            return result.get('order_id')

        except OkexAPIException as e:
            logger.error('OkexAPIException:%s, %s',e.status_code,e.response.text)

            obj = e.response.json()

            code = rest_code(obj.get('code'))

            raise FailException(code,obj.get('message'))

        

    def limit_orders_appender(self ,orders, price ,amount , side , coin , currency):    

        otype = 'limit'
        instrument_id = '%s-%s' % (coin,currency)
        size = '%s' % amount  
        price = '%s' % price 
        
        return self.spotApi.orders_appender(orders, otype,side,instrument_id,size,price=price)


    def limit_orders(self, orders ):
        
        logger.debug('limit_orders, start .. ')
        
        result = self.spotApi.take_orders(orders)

        logger.debug('limit_orders, resp : %s' , result )

        return result

    def market_buy(self, volume , coin , currency ):

        otype = 'market'
        side = 'buy'
        instrument_id = '%s-%s' % (coin,currency)
        funds = '%s' % volume

        try:
            result = self.spotApi.take_order(otype,side,instrument_id,funds=funds)

            logger.debug('market_buy, resp : %s' , result )

            return result.get('order_id')

        except OkexAPIException as e:
            logger.error('OkexAPIException:%s, %s',e.status_code,e.response.text)

            obj = e.response.json()

            code = rest_code(obj.get('code'))

            raise FailException(code,obj.get('message'))

 

    def market_sell(self, amount , coin , currency):

        otype = 'market'
        side = 'sell'
        instrument_id = '%s-%s' % (coin,currency)
        size = '%s' % amount  
        
        try:
            result = self.spotApi.take_order(otype,side,instrument_id,size=size)

            logger.debug('market_sell, resp : %s' , result )

            return result.get('order_id')

        except OkexAPIException as e:
            logger.error('OkexAPIException:%s, %s',e.status_code,e.response.text)

            obj = e.response.json()

            code = rest_code(obj.get('code'))

            raise FailException(code,obj.get('message'))

 

    def cancel_order(self, orderid, coin,currency ):

        instrument_id = '%s-%s' % (coin,currency)
        try:
            result = self.spotApi.revoke_order(orderid , instrument_id )

            logger.debug('cancel order, resp : %s' , result )

            return result

        except OkexAPIException as e:

            logger.error('OkexAPIException:%s, %s',e.status_code,e.response.text)

            obj = e.response.json()

            code = rest_code(obj.get('code'),40600)

            raise FailException(code,obj.get('message'))



        