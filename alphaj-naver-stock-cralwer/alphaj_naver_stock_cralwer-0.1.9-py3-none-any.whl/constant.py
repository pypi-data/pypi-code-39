class Constant(object):
    RETRY = 10
    CURRENT_Q = '2019/03'
    SHEET_NAME_MAP = {
        'balance_sheet': '대차대조표 (5년)'
        , 'balance_sheet_recent': '대차대조표 (최근 4분기)'
        , 'income_sheet': '손익계산서 (5년)'
        , 'income_sheet_recent': '손익계산서 (최근 4분기)'
        , 'cashflow_sheet': '현금흐름표 (5년)'
        , 'cashflow_sheet_recent': '현금흐름표 (최근 4분기)'
        , 'profitability_sheet': '수익성지표 (5년)'
        , 'profitability_sheet_recent': '수익성지표 (최근 4분기)'
        , 'stability_sheet': '안정성지표 (5년)'
        , 'stability_sheet_recent': '안정성지표 (최근 4분기)'
        , 'active_sheet': '활동성지표 (5년)'
        , 'active_sheet_recent': '활동성지표 (최근 4분기)'
        , 'value_sheet': '가치지표 (5년)'
        , 'value_sheet_recent': '가치지표 (최근 4분기)'
    }

class URL(object):
    MARKET_CAP_URL = 'http://finance-service.daum.net/item/quote.daum?code='
    DAUM_PRICE_URL = 'http://finance-service.daum.net//item/quote_yyyymmdd_sub.daum?code={}&modify=1'