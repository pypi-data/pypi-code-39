import requests

from bitfex_api import Api, ApiResponse

def test_constructor():
  api = Api()
  assert api is not None
  assert api._server_url == 'https://bitfex.trade'

def test_constructor_with_params():
  api = Api('server')
  assert api._server_url == 'server'

def test_user_no_token():
  api = Api('https://server')
  response = api.user()
  assert response.success is False
  assert response.error == 'NOT_AUTHORIZED'

def test_user_wrong_token(requests_mock):
  requests_mock.get("https://server/api/v1/user", json={'success': False, 'error': 'WRONG_REQUEST'})
  api = Api('https://server')
  api._token = 'qwe123'
  response = api.user()
  assert response.success is False
  assert response.error == 'WRONG_REQUEST'

def test_user_success(requests_mock):
  requests_mock.get("https://server/api/v1/user", json={'success': True, 'username': 'USER', 'balances': {'BTC': 0}})
  api = Api('https://server')
  api._token = 'mock_correct_token'
  response = api.user()
  assert response.success is True
  assert response.response['username'] == 'USER'
  assert response.response['balances']['BTC'] == 0

def test_orders_my_no_token():
  api = Api('https://server')
  response = api.orders_my()
  assert response.success is False
  assert response.error == 'NOT_AUTHORIZED'

def test_orders_my_wrong_token(requests_mock):
  requests_mock.get("https://server/api/v1/orders/my", json={'success': False, 'error': 'Not authorized'})
  api = Api('https://server')
  api._token = 'qwe123'
  response = api.orders_my()
  assert response.success is False
  assert response.error == 'Not authorized'

def test_orders_my_success(requests_mock):
  requests_mock.get("https://server/api/v1/orders/my", json={'success': True, 'orders': []})
  api = Api('https://server')
  api._token = 'qwe123'
  response = api.orders_my()
  assert response.success is True
  assert response.response['orders'] == []

def test_orders_success(requests_mock):
  requests_mock.get("https://server/api/v1/orders?pair=BTC_RUR", json={'success': True, 'orders': []})
  api = Api('https://server')
  response = api.orders('BTC_RUR')
  assert response.success is True
  assert response.response['orders'] == []

def test_create_order_no_token():
  api = Api()
  response = api.create_order('BTC_RUR', 'buy', 1.0, 1.0)
  assert response.success is False
  assert response.error == 'NOT_AUTHORIZED'

def test_create_order_wrong_token():
  api = Api()
  response = api.create_order('BTC_RUR', 'buy', 1.0, 1.0)
  assert response.success is False
  assert response.error == 'NOT_AUTHORIZED'

def test_create_order_success_not_full(requests_mock):
  requests_mock.post("https://server/api/v1/orders", json={'success': True, 'order_id': 1})
  api = Api('https://server')
  api._token = 'qwe123'
  response = api.create_order(pair = 'BTC_RUR', operation = 'buy', amount = 1.0, price = 10.0)
  assert response.success is True
  assert response.response['order_id'] == 1

def test_create_order_success_full(requests_mock):
  requests_mock.post("https://server/api/v1/orders", json={'success': True})
  api = Api('https://server')
  api._token = 'qwe123'
  response = api.create_order(pair = 'BTC_RUR', operation = 'buy', amount = 1.0, price = 10.0)
  assert response.success is True
  assert response.response['order_id'] is None