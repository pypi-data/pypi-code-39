import requests
from typing import NamedTuple, Optional

class ApiResponse(NamedTuple):
  success: bool
  response: Optional[dict] = None
  error: Optional[str] = None

class Api:
  _server_url: str = "https://bitfex.trade"

  _token: Optional[str] = None

  def __init__(self, server_url: str = None, token: str = None):
    """
    BitFex.Trade API wrapper

    :param server_url: Base API server url, defaults to 'https://bitfex.trade'
    :param token: API token, defaults to None
    """
    if server_url is not None:
      self._server_url = server_url

    if token is not None:
      self._token = token

  def user(self) -> ApiResponse:
    """
    Return information about current user

    :return: User information (username, balances)
    :rtype: ApiResponse

    :Example:

    >>> api.user()
    ApiResponse(success = True, response = {'username': 'USERNAME', 'balances': {'BTC': 0, 'USD': 1.0}})
    >>> api.user()
    ApiResponse(success = False, error = 'NOT_AUTHORIZED')
    >>> api.user()
    ApiResponse(success = False, error = 'WRONG_REQUEST')
    """
    if self._token is None:
      return ApiResponse(success = False, error = 'NOT_AUTHORIZED')

    response = self._send_request(self._server_url, 'GET', self._token, '/api/v1/user')

    if response.get('success') is True:
      return ApiResponse(success = True, response = {
        'username': response.get('username'),
        'balances': response.get('balances')
      })
    
    return ApiResponse(success = False, error = response.get('error'))

  def orders_my(self) -> ApiResponse:
    """
    My active orders list

    :return: Currently active orders
    :rtype: ApiResponse

    :Example:

    >>> api.orders_my()
    ApiResponse(success = True, response = [])
    >>> api.orders_my()
    ApiResponse(success = True, response = [{'id':1,'pair':'BTC_RUR','amount': 1.0,'price':600000.0,'operation':'sell','completed':False,'updated':1562287274000,'user_id':'n23'}])
    >>> api.orders_my()
    ApiResponse(success = False, error = 'NOT_AUTHORIZED')
    >>> api.orders_my()
    ApiResponse(success = False, error = 'WRONG_REQUEST')
    """
    if self._token is None:
      return ApiResponse(success = False, error = 'NOT_AUTHORIZED')

    response = self._send_request(self._server_url, 'GET', self._token, '/api/v1/orders/my')

    if response.get('success') is True:
      return ApiResponse(success = True, response = {
        'orders': response.get('orders')
      })

    return ApiResponse(success = False, error = response.get('error'))

  def orders(self, pair: str) -> ApiResponse:
    """
    Return orders list for pair

    :return: Orders for pair
    :rtype: ApiResponse

    :Example:

    >>> api.orders('BTC_USD')
    ApiResponse(success = True, response = [])
    >>> api.orders('BTC_RUR')
    ApiResponse(success = True, response = [{'id':1,'pair':'BTC_RUR','amount': 1.0,'price':600000.0,'operation':'sell','completed':False,'updated':1562287274000,'user_id':'n23'}])
    """
    response = self._send_request(self._server_url, 'GET', self._token, f"/api/v1/orders?pair={pair}")

    if response.get('success') is True:
      return ApiResponse(success = True, response = {
        'orders': response.get('orders')
      })

    return ApiResponse(success = False, error = response.get('error'))

  def create_order(self, pair: str, operation: str, amount: float, price: float) -> ApiResponse:
    """
    Create order

    :param pair: pair, for example 'BTC_RUR'
    :param operation: 'buy' or 'sell'
    :param amount: order amount, for example 1.0
    :param price: order price, for example 10.0

    :rtype: ApiResponse

    :Example:

    >>> api.create_order(pair = 'BTC_RUR', operation = 'buy', amount = 1.0, price = 10.0)
    ApiResponse(success = True) # fully completed
    >>> api.create_order(pair = 'BTC_RUR', operation = 'buy', amount = 1.0, price = 10.0)
    ApiResponse(success = True, response = {'order_id': 1}) # not fully completed
    >>> api.create_order(pair = 'BTC_RUR', operation = 'buy', amount = 1.0, price = 10.0)
    ApiResponse(success = False, error: 'NOT_AUTHORIZED') # no token
    """
    if self._token is None:
      return ApiResponse(success = False, error = 'NOT_AUTHORIZED')

    response = self._send_request(self._server_url, 'POST', self._token, '/api/v1/orders')

    if response.get('success') is True:
      return ApiResponse(success = True, response = {
        'order_id': response.get('order_id')
      })

    return ApiResponse(success = False, error = response.get('error'))

  def cancel_order(self, order_id: int) -> ApiResponse:
    """
    Cancel order

    :param order_id: order id
    :rtype: ApiResponse

    :Example:

    >>> api.cancel_order(1)
    ApiResponse(success = True)
    """
    if self._token is None:
      return ApiResponse(success = False, error = 'NOT_AUTHORIZED')

    response = self._send_request(self._server_url, 'POST', self._token, '/api/v1/orders')

    if response.get('success') is True:
      return ApiResponse(success = True, response = {
        'order_id': response.get('order_id')
      })

    return ApiResponse(success = False, error = response.get('error'))

  def _send_request(self, server: str, method: str = 'GET', token: Optional[str] = None, endpoint: str = '/', body: dict = None) -> dict:
    """
    Send request to API
    """
    request_method = None
    headers = {
      'Content-Type': 'application/json'
    }

    if method == 'POST':
      request_method = requests.post
    if method == 'GET':
      request_method = requests.get

    headers['X-Api-Key'] = token

    if request_method is not None:
      return request_method("".join([server, endpoint]), headers=headers, json=body).json()
    else:
      return {'success': False, 'error': 'WRONG_REQUEST'}
