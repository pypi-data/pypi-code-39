#-*- coding: utf-8 -*-
__author__  = "8034.com"
__date__    = "2019-07-02"

import sys
import os
import xmind
from xmind.core import workbook,saver
from xmind.core.topic import TopicElement
import json
import xlrd
import xlwt
from xlutils.copy import copy as xlscopy



class XmindParse(object):
    source_xmind_file = None
    xmind_workbook = None

    def __init__(self, xmind_path):
        self.source_xmind_file = xmind_path
        self.xmind_workbook = xmind.load(self.source_xmind_file)
        if not self.xmind_workbook: 
            raise Exception("xmind文件解析异常。请确认xmind文件路径.")
        pass

    def get_sheet_by_name(self, sheet_name):
        for sheet in self.xmind_workbook.getSheets():
            if sheet.getTitle() == sheet_name:
                return sheet
        return None

    def get_primary_sheet(self):
        return self.xmind_workbook.getPrimarySheet()

    def show_sheets_info(self):
        xmind_workbook_info = {}
        index = 0
        for sheet in self.xmind_workbook.getSheets():
            xmind_workbook_info[index] = sheet.getTitle()
            index = index + 1
        return xmind_workbook_info

    def generate_sheets(self):
        for sheet in self.xmind_workbook.getSheets():
            yield sheet.getTitle(), sheet


    def get_ponit_info(self, topic):
        point = {}
        point["title"] = topic.getTitle() # xmind 标题 
        point["notes"] = topic.getNotes()  # xmind 备注
        point["marker"]= None
        if topic.getMarkers():
            topic_marker_id = topic.getMarkers()[0].getMarkerId() # xmind 标签(优先级)
            topic_marker_name = self.switch_priority(topic_marker_id) 
            point["marker"]= topic_marker_name
        return point

    def parse_topic_tree(self, _root_topic, _to_excel_row):
        _point_info = self.get_ponit_info(_root_topic)
        _to_excel_row.append(_point_info)

        sub_topic_list = _root_topic.getSubTopics()  # get all sub topic
        if not sub_topic_list :
            yield _to_excel_row
        else:
            for topic in sub_topic_list:
                copy_to_excel_row = _to_excel_row.copy()
                to_excel_row = self.parse_topic_tree(topic, copy_to_excel_row)
                for i in to_excel_row:
                    # print("inner parse_topic_tree.to_excel_row >> {}".format(i))
                    yield i
                pass
            pass
        pass

    def parse_sheet(self, sheet):
        to_excel_row = []
        root_topic = sheet.getRootTopic() # get the root topic of this sheet
        # self.parse_topic_tree(root_topic, to_excel_row)
        to_excel_row = self.parse_topic_tree(root_topic, to_excel_row)
        # for i in to_excel_row:
            # print("parse_xmind.to_excel_row >> {}".format(i))
        return to_excel_row

    def switch_priority(self,xmind_priority):
        if (xmind_priority == "priority-1"):
            return u"高"
        elif (xmind_priority == "priority-2"): 
            return u"中"
        elif (xmind_priority == "priority-3"): 
            return u"低"
        else:
            return  u"中"


if __name__ =="__main__":
    xmind_path= u"D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\example_0.3.0.xmind"
    xmindParse = XmindParse(xmind_path)
    print(xmindParse.show_sheets_info()) 
    # print(xmindParse.get_primary_sheet()) 
    sheet = xmindParse.get_sheet_by_name("画布 1")
    primary = xmindParse.get_primary_sheet()
    xmindParse.parse_sheet(primary)
    pass

