import pandas as pd
from datetime import datetime, timedelta
from alphaj_naver_stock_info_crawler.constant import Constant
import math
from alphaj_naver_stock_info_crawler.Util import floatOrZero

CURRENT_Q = Constant.CURRENT_Q

def pcr(stock):
    if 'cash_flow_sheet_recent' in stock:
        try:
            operating_cashflow = stock['cash_flow_sheet_recent']['DATA']['영업활동으로인한현금흐름']
            pcr = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(operating_cashflow[CURRENT_Q])
            if math.isnan(pcr):
                return -9999
            else:
                return pcr
        except Exception as e:
            return -9999
    else:
        return -9999

def psr(stock):
    
    if 'profitablity_sheet_recent' in stock:
        try:
            revenue = stock['profitablity_sheet_recent']['DATA']['매출액＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(revenue[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In PSR: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        return -9999

def por(stock):
    
    if 'profitablity_sheet_recent' in stock:
        try:
            operating_income = stock['profitablity_sheet_recent']['DATA']['영업이익＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(operating_income[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In POR: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        try:
            operating_income = stock['profitability_sheet_recent']['DATA']['영업이익＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(operating_income[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In POR: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999

def per(stock):
    
    if 'profitability_sheet_recent' in stock:
        try:
            net_profit = stock['profitability_sheet_recent']['DATA']['당기순이익(지배)＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(net_profit[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In PER: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        try:
            net_profit = stock['profitability_sheet_recent']['DATA']['당기순이익(지배)＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(net_profit[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In PER: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999

def ev(stock):
    try:
        net_debt = stock['balance_sheet_recent']['DATA']['*순부채']
        value = floatOrZero(stock['quant_data']['market_capital']) - net_debt[constants.CURRENT_Q]
        if math.isnan(value):
            return -9999
        else:
            return value
    except:
        return -9999


def ev_ebit(stock):
    try:
        ev_value = ev(stock)

        ebit_value = get_item_current_q(stock, 'income_sheet_recent', '*ebit')


        value = ev_value / ebit_value
        if math.isnan(value):
            return -9999
        else:
            return value
    except:
        return -9999

def pbr(stock):
    if 'profitability_sheet_recent' in stock:
        try:
            total_equity = stock['profitability_sheet_recent']['DATA']['자본총계(지배)＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(total_equity[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In PBR: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        try:
            total_equity = stock['profitability_sheet_recent']['DATA']['자본총계(지배)＜당기＞']
            value = floatOrZero(stock['quant_data']['market_capital']) / floatOrZero(total_equity[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In PBR: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999

def roe(stock):
    
    if 'profitability_sheet_recent' in stock:
        try:
            net_profit = stock['profitability_sheet_recent']['DATA']['당기순이익(지배)＜당기＞']
            total_equity = stock['profitability_sheet_recent']['DATA']['자본총계(지배)＜당기＞']
            value = floatOrZero(net_profit[CURRENT_Q]) / floatOrZero(total_equity[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In ROE: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        try:
            net_profit = stock['profitability_sheet_recent']['DATA']['당기순이익(지배)＜당기＞']
            total_equity = stock['profitability_sheet_recent']['DATA']['자본총계(지배)＜당기＞']
            value = floatOrZero(net_profit[CURRENT_Q]) / floatOrZero(total_equity[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In ROE: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999

def roa(stock):
    if 'profitability_sheet_recent' in stock:
        try:
            net_profit = stock['profitability_sheet_recent']['DATA']['당기순이익(지배)＜당기＞']
            total_asset = stock['profitability_sheet_recent']['DATA']['자산총계＜당기＞']
            value = floatOrZero(net_profit[CURRENT_Q]) / floatOrZero(total_asset[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In ROA: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        try:
            net_profit = stock['profitability_sheet_recent']['DATA']['당기순이익(지배)＜당기＞']
            total_asset = stock['profitability_sheet_recent']['DATA']['자산총계＜당기＞']
            value = floatOrZero(net_profit[CURRENT_Q]) / floatOrZero(total_asset[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In ROA: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999

def gpa(stock):
    if 'profitability_sheet_recent' in stock:
        try:
            gross_margin = stock['profitability_sheet_recent']['DATA']['매출총이익＜당기＞']
            total_asset = stock['profitability_sheet_recent']['DATA']['자산총계＜당기＞']
            value = floatOrZero(gross_margin[CURRENT_Q]) / floatOrZero(total_asset[CURRENT_Q])
            if math.isnan(value):
                return -9999
            else:
                return value
        except Exception as e:
            print("In GPA: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999
    else:
        try:
            gross_margin = stock['profitability_sheet_recent']['DATA']['매출총이익＜당기＞']
            total_asset = stock['profitability_sheet_recent']['DATA']['자산총계＜당기＞']
            return floatOrZero(gross_margin[CURRENT_Q]) / floatOrZero(total_asset[CURRENT_Q])
        except Exception as e:
            print("In GPA: " + stock['quant_data']['stock_name'] +
                  " " + stock['quant_data']['stock_code'] + " " + str(e))
            return -9999


def get_average_trading_value(stock, N_days):
    if not stock['price_data']:
        return -1

    df = pd.read_json(stock['price_data'])

    # print(df.columns)

    before_price_maximum_trial = 30
    current_price_maximum_trial = 30

    before_price_trial = 0
    current_price_trial = 0

    current_day_offset = 0

    current_day = datetime.now()
    while True:

        current_day = datetime.now() - timedelta(days=current_day_offset)

        try:
            # print("current_date", current_day.strftime("%Y-%m-%d"))
            current_price = float(
                df.loc[current_day.strftime("%Y-%m-%d")]['Close'])
            break
        except:
            # print("exception current_date")
            current_day_offset = current_day_offset + 1
            current_price_trial = current_price_trial + 1
            if current_price_trial >= current_price_maximum_trial:
                # print("Time over!")
                return -1
                break

    # print(N_days, momentum_value)

    total_count = 0
    total_trading_value = 0

    for i in range(N_days):
        current_day = datetime.now() - timedelta(days=i)
        try:
            volume = float(df.loc[current_day.strftime("%Y-%m-%d")]['Volume'])
            price = float(df.loc[current_day.strftime("%Y-%m-%d")]['Close'])

            total_trading_value += volume * price
            total_count += 1
        except:
            continue

    print(total_trading_value / total_count)
    return total_trading_value / total_count

    return get_average_trading_value


def momentum(stock, N_days):
    if not stock['price_data']:
        return -1

    df = pd.read_json(stock['price_data'])

    # print(df.columns)

    before_price_maximum_trial = 30
    current_price_maximum_trial = 30

    before_price_trial = 0
    current_price_trial = 0

    current_day_offset = 0

    while True:

        date_N_days_ago = datetime.now() - timedelta(days=N_days)
        current_day = datetime.now() - timedelta(days=current_day_offset)

        try:
            # print("before_date", date_N_days_ago.strftime("%Y-%m-%d"))
            before_price = float(
                df.loc[date_N_days_ago.strftime("%Y-%m-%d")]['Close'])
        except:
            # print("exception before_date")
            N_days = N_days+1
            before_price_trial = before_price_trial + 1
            if before_price_trial >= before_price_maximum_trial:
                # print("Time over!")
                momentum_value = -1
                break
            continue

        try:
            # print("current_date", current_day.strftime("%Y-%m-%d"))
            current_price = float(
                df.loc[current_day.strftime("%Y-%m-%d")]['Close'])
        except:
            # print("exception current_date")
            current_day_offset = current_day_offset + 1
            current_price_trial = current_price_trial + 1
            if current_price_trial >= current_price_maximum_trial:
                # print("Time over!")
                momentum_value = -1
                break
            continue

        momentum_value = current_price / before_price
        if momentum_value > 0:
            break
    # print(N_days, momentum_value)

    return momentum_value
