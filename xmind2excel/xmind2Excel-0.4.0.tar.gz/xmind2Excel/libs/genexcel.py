#-*- coding: utf-8 -*-
__author__  = "8034.com"
__date__    = "2018-10-22"

import sys
import xlwt

from .xmindparse import XmindParse

class GenerateExcel(object):
    dist_excel_file = None
    excel_workbook = None

    def __init__(self, excel_path):
        self.excel_workbook = xlwt.Workbook()
        self.dist_excel_file = excel_path
        # ws = w.add_sheet('1') #创建一个工作表
        pass
 
    def genExcel(self, xmindParse):
        for name, sheet in xmindParse.generate_sheets():
            print("name={}, sheet= {}".format(name, sheet))
            sheet_row_generator = xmindParse.parse_sheet(sheet)
            self.gen_sheet(name, sheet_row_generator)
            pass
        return self

    def gen_sheet(self, sheet_name, sheet_row_generator):
        print("新 sheet {}".format (sheet_name))
        sheet_temp = self.excel_workbook.add_sheet(sheet_name)
        row = 1
        for row_info in sheet_row_generator:
            print(row_info)
            for col_num in range(len(row_info)):
                # print(">>>>> {}".format (col_num))
                sheet_temp.write(row,col_num,row_info[col_num]["title"]) 
                # sheet_temp.write(row,col_num,row_info[col_num]["title"], "style") # 带样式的写入
                pass
            pass
            row = row + 1
        return self

    def save(self):
        self.excel_workbook.save(self.dist_excel_file)
        return self

    def main(self,xmind_path):
        # xmind_path= u"D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\example_0.3.0.xmind"
        # excel_path= u"D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\ttoo.xls"
        xmindParse = XmindParse(xmind_path)
        self.genExcel(xmindParse)
        self.save()
        return "OK"

    pass


if __name__ =="__main__":
    xmind_path= u"D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\example_0.3.0.xmind"
    excel_path= u"D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\ttoo.xls"

    xmindParse = XmindParse(xmind_path)

    generateexcel = GenerateExcel(excel_path)
    generateexcel.genExcel(xmindParse)
    generateexcel.save()

    pass
