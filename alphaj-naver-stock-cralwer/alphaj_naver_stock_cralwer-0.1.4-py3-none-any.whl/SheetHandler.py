import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from alphaj_naver_stock_info_crawler.Util import (
    read_json, convert_nan)
from alphaj_naver_stock_info_crawler.Validator import (
    check_valid_stock_name, check_valid_stock_code
)
from ..constant import (
    Constant,
    URL
)
from alphaj_naver_stock_info_crawler.PriceCralwer import (DaumPriceCralwer)

from alphaj_naver_stock_info_crawler.Valuation import *

import requests
import unidecode

def get_recent_sheet_json(stock_code, stock_name, sheet_name):
    file_name = './jsons/sheets/last/{}_{}_{}.json'.format(
        stock_code, stock_name, sheet_name)
    json_data = read_json(file_name)

    return json_data


def get_all_recent_sheet_json(stock_code, stock_name):
    balance_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'balance_sheet')

    income_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'income_sheet')

    cashflow_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'cashflow_sheet')

    active_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'active_sheet')

    growth_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'growth_sheet')

    profitability_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'profitability_sheet')

    stability_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'stability_sheet')

    value_sheet_obj = get_recent_sheet_json(
        stock_code, stock_name, 'value_sheet')

    return {
        'balance_sheet_obj': balance_sheet_obj, 'income_sheet_obj': income_sheet_obj, 'cashflow_sheet_obj': cashflow_sheet_obj, 'active_sheet_obj': active_sheet_obj, 'profitability_sheet_obj': profitability_sheet_obj, 'growth_sheet_obj': growth_sheet_obj, 'stability_sheet_obj': stability_sheet_obj, 'value_sheet_obj': value_sheet_obj
    }


def get_dividend(code):
    url = "http://wisefn.stock.daum.net/company/c1010001.aspx?cmp_cd=%s&frq=&rpt=" % (
        code)

    html = requests.get(url).text

    df_list = pd.read_html(html)
    df = df_list[0]
    # print(df.ix[4].ix[0])

    str = unidecode.unidecode(df.loc[4].loc[0])
    split = str.split('|')

    if len(split[5].split()) == 1:
        dividend = -9999
    else:
        dividend = split[5].split()[1].rstrip('%')

    # print(split)
    # ret = {
    #     # 'PER': split[2].split()[1].replace(',', ''),
    #     # 'PBR': split[4].split()[1].replace(',', ''),
    #     'dividend': dividend
    # }

    print("dividend: ", dividend)
    return dividend


def get_stock_all_information(stock_code, stock_name):
    stock_object = {}

    if check_valid_stock_code(stock_code) and check_valid_stock_name(stock_name):
        sheets = get_all_recent_sheet_json(stock_code, stock_name)

        market_capital_url = "{}{}".format(URL.MARKET_CAP_URL, stock_code)

        tables = pd.read_html(market_capital_url)

        market_captial = tables[0].loc[9][1]

        number_of_share = tables[0].loc[10][1]

        [today_price, dod, mom, yoy, today_volume, average_volume,
            price_data] = DaumPriceCralwer().get_price_data(stock_code, 1)
        price_data = pd.read_json(price_data)
        price_data_json = price_data.to_json()

        stock_object = {}

        stock_object['balance_sheet'] = sheets['balance_sheet_obj']['balance_sheet']
        stock_object['balance_sheet_recent'] = sheets['balance_sheet_obj']['balance_sheet_recent']
        stock_object['income_sheet'] = sheets['income_sheet_obj']['income_sheet']
        stock_object['income_sheet_recent'] = sheets['income_sheet_obj']['income_sheet_recent']
        stock_object['cashflow_sheet'] = sheets['cashflow_sheet_obj']['cashflow_sheet']
        stock_object['cashflow_sheet_recent'] = sheets['cashflow_sheet_obj']['cashflow_sheet_recent']
        stock_object['active_sheet'] = sheets['active_sheet_obj']['active_sheet']
        stock_object['active_sheet_recent'] = sheets['active_sheet_obj']['active_sheet_recent']
        stock_object['profitability_sheet'] = sheets['profitability_sheet_obj']['profitability_sheet']
        stock_object['profitability_sheet_recent'] = sheets['profitability_sheet_obj']['profitability_sheet_recent']
        stock_object['stability_sheet'] = sheets['stability_sheet_obj']['stability_sheet']
        stock_object['stability_sheet_recent'] = sheets['stability_sheet_obj']['stability_sheet_recent']
        stock_object['value_sheet'] = sheets['value_sheet_obj']['value_sheet']
        stock_object['value_sheet_recent'] = sheets['value_sheet_obj']['value_sheet_recent']
        stock_object['quant_data'] = {}
        stock_object['quant_data']['stock_code'] = stock_code
        stock_object['quant_data']['stock_name'] = stock_name
        stock_object['quant_data']['dividend'] = get_dividend(stock_code)
        stock_object['quant_data']['market_capital'] = market_captial
        stock_object['quant_data']['number_of_share'] = number_of_share
        stock_object['price_data'] = price_data_json
        stock_object['quant_data']['today_price'] = today_price
        stock_object['quant_data']['dod'] = dod
        stock_object['quant_data']['mom'] = mom
        stock_object['quant_data']['yoy'] = yoy
        stock_object['quant_data']['today_volume'] = today_volume
        stock_object['quant_data']['average_volume'] = average_volume
        stock_object['quant_data']['per'] = convert_nan(per(stock_object))
        stock_object['quant_data']['por'] = convert_nan(por(stock_object))
        stock_object['quant_data']['psr'] = convert_nan(psr(stock_object))
        stock_object['quant_data']['pcr'] = convert_nan(pcr(stock_object))
        stock_object['quant_data']['gpa'] = convert_nan(gpa(stock_object))
        stock_object['quant_data']['roe'] = convert_nan(roe(stock_object))
        stock_object['quant_data']['roa'] = convert_nan(roa(stock_object))
        stock_object['quant_data']['pbr'] = convert_nan(pbr(stock_object))
        stock_object['quant_data']['ev'] = convert_nan(ev(stock_object))
        stock_object['quant_data']['ev_ebit'] = convert_nan(ev_ebit(stock_object))
        for i in range(10):
            stock_object['quant_data']['momentum_3'] = momentum(stock_object, 90)
            stock_object['quant_data']['momentum_6'] = momentum(stock_object, 180)
            stock_object['quant_data']['momentum_9'] = momentum(stock_object, 270)
            stock_object['quant_data']['momentum_12'] = momentum(stock_object, 365)

    return stock_object
