import json
import pandas as pd
from alphaj_naver_stock_info_crawler.constant import (
    Constant
)

def save_all_stock_information_to_excel(stock_object, file_name):

    wbw = pd.ExcelWriter(file_name)



    for key in stock_object:
        if key in Constant.SHEET_NAME_MAP:
            korean_name = Constant.SHEET_NAME_MAP[key]
            print(korean_name)
            sheet_obj = stock_object[key]

            df = pd.read_json(json.dumps(sheet_obj['DATA']), orient='index')

            df.fillna('', inplace=True)

            print(df)


            df.to_excel(wbw, korean_name)

    wbw.save()


