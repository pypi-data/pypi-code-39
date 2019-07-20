
import alphaj_naver_stock_info_crawler.SheetHandler as sheet_handler

import alphaj_naver_stock_info_crawler.ExcelHandler as excel_handler

__all__ = ['ExcelHandler', 'SheetHandler']
__version__ = '0.1.1'

def get_stock_all_information_json(stock_code, stock_name):
    return sheet_handler.get_stock_all_information(stock_code, stock_name)

def save_stock_all_information_to_excel(stock_code, stock_name, file_name = None):
    stock_object = sheet_handler.get_stock_all_information(stock_code, stock_name)
    if file_name == None:
        file_name = '{}_{}.xlsx'.format(stock_code, stock_name)
    if not file_name.endswith('.xlsx'):
        file_name = file_name + ".xlsx"
    excel_handler.save_all_stock_information_to_excel(stock_object, file_name)
