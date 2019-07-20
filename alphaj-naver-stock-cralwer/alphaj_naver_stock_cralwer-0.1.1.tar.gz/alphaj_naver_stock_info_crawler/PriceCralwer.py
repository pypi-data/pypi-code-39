from constant import (URL)
import pandas as pd
def get_N_days_before_volume(N_days, df):
    
    current_price_maximum_trial = 30

    current_price_trial = 0

    current_day_offset = 0

    isDone = False

    current_price = -9999
    while True:
        try:
            current_day = datetime.now() - timedelta(days=N_days)
            current_price = int(
                df.loc[current_day.strftime("%Y-%m-%d")]['Volume'])
        except:
            N_days = N_days + 1
            current_price_trial = current_price_trial + 1
            if current_price_trial >= current_price_maximum_trial:
                break
            continue

        isDone = True
        break
    if isDone:
        return current_price
    else:
        return -9999

def get_N_days_before_price(N_days, df):
    
    # print(df.tail())

    current_price_maximum_trial = 30

    current_price_trial = 0

    current_day_offset = 0

    isDone = False

    current_price = -9999
    while True:
        try:
            current_day = datetime.now() - timedelta(days=N_days)
            # print(current_day.strftime("%Y-%m-%d"))
            current_price = float(
                df.loc[current_day.strftime("%Y-%m-%d")]['Close'])
        except Exception as e:
            # print("getNdayBeforePrice", str(e), current_day)
            N_days = N_days + 1
            current_price_trial = current_price_trial + 1
            if current_price_trial >= current_price_maximum_trial:
                break
            continue

        isDone = True
        break
    if isDone:
        return current_price
    else:
        return -9999

class PriceCralwer(object):
    # def __init__():
    #     pass

    def get_price_data(stock_code, page_no):
        raise NotImplementedError()

class DaumPriceCralwer(PriceCralwer):
    # # def __init__(self):
    #     # super.__init__(self)
    #     pass
    
    def get_price_data(self, stock_code, page_no):
        url = URL.DAUM_PRICE_URL.format(stock_code)


        df = pd.DataFrame()

        for page in range(1, page_no+1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

        df = df.dropna()

        df = df.rename(columns= {'일자': 'Date', '종가': 'Close', '전일비': 'Diff', '시가': 'Open', '고가': 'High', '저가': 'Low', '거래량': 'Volume', '등락률': 'UpDown'})

        df[['Close', 'Open', 'High', 'Low', 'Volume']]  = df[['Close', 'Open', 'High', 'Low', 'Volume']].astype(int) 

        df['Date'] = pd.to_datetime(df['Date'], format="%y.%m.%d")

        df = df.sort_values(by=['Date'], ascending=False)

        df = df.set_index('Date')

        df.index = df.index.strftime("%Y-%m-%d")
        df = df[~df.index.duplicated(keep='last')]

        today_price = get_N_days_before_price(0, df)

        yesterday_price = get_N_days_before_price(1, df)

        month_before_price = get_N_days_before_price(30, df)

        year_before_price = get_N_days_before_price(365, df)

        today_volume = get_N_days_before_volume(0, df)

        average_volume = 0

        DoD = today_price / yesterday_price

        MoM = today_price / month_before_price

        YoY = today_price / year_before_price

        json = df.to_json()

        return [today_price, DoD, MoM, YoY, today_volume, average_volume, json]
