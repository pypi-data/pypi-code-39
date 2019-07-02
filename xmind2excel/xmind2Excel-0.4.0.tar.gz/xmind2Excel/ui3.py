# -*- coding: utf-8 -*-
__author__  = "8034.com"
__date__    = "2018-11-08"

import sys
import os, time

# python3.X
from tkinter import *
from tkinter import messagebox, filedialog

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

def file_extension(path): 
    return os.path.splitext(path)[1] 
def file_name(path): 
    return os.path.splitext(path)[0] 
    
class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)

    def selectXmindFile(self):
        string_filename=""
        # print((os.path.join(FILE_PATH, 'templet')))
        # print((os.path.join(FILE_PATH, 'templet')))
        
        # filenames = filedialog.askopenfilename(initialdir=(os.path.join(FILE_PATH, 'templet')))
        filenames = filedialog.askopenfilename() # 系统默认路径
        print(filenames)
        if len(filenames) != 0:
            string_filename =filenames
            text = u"您选择的文件是："+string_filename
        else:
            text = u"您没有选择任何文件"
        print(text)
        self.xmind_Text.delete(0.0,END)
        self.xmind_Text.insert(1.0,string_filename if string_filename else text)

        src_path = os.path.dirname(string_filename)
        excel_file = os.path.join(src_path, "to-{}.xls".format(int(round(time.time() * 1000))))
        excel_file=excel_file.replace("\\","/")
        self.excel_file_Text.delete(0.0,END)
        self.excel_file_Text.insert(1.0,excel_file)
        return string_filename



    def toexcel(self):
        xmind_Text_content=(self.xmind_Text.get('1.0',END)).strip()
        excel_file_Text_content=(self.excel_file_Text.get('1.0',END)).strip()

        result = "running..."

        from xmind2Excel.libs.genexcel import GenerateExcel
        xmindParse = GenerateExcel(excel_file_Text_content)
        result = xmindParse.main(xmind_Text_content)
        
        self.sp05_Label.config(text=result)
        print("**"*10)
        return "ok"


    def createWidgets(self,master=None):

        self.frame_1 = Frame(master)
        self.xmind_Text = Text(self.frame_1,height="1",width="60")
        self.xmind_Text.pack(side=LEFT, expand=YES)
        self.xmind_Text.insert(INSERT,u"xmind Path")
        self.sp01_Label = Label(self.frame_1, text=u'<==', height="1",width="5")
        self.sp01_Label.pack(side=LEFT, expand=YES)
        self.select_file_button = Button(self.frame_1, text=u'选择文件', command = self.selectXmindFile )
        self.select_file_button.pack()
        self.frame_1.pack(side=TOP)

        self.frame_2 = Frame(master)
        self.excel_file_Text = Text(self.frame_2,height="1",width="60")
        self.excel_file_Text.pack(side=LEFT, expand=YES)
        self.excel_file_Text.insert(INSERT,u"目标路径")
        self.sp02_Label = Label(self.frame_2, text=u'<==', height="1",width="5")
        self.sp02_Label.pack(side=LEFT, expand=YES)
        self.excel_file_Label = Label(self.frame_2, text=u'生成xls ', height="1")
        self.excel_file_Label.pack()
        self.frame_2.pack(side=TOP)


        self.frame_4 = Frame(master)
        self.change_toxlsx_Button = Button(self.frame_4, text='TO Excel',state='normal',command=self.toexcel)
        self.change_toxlsx_Button.pack(side=LEFT, expand=YES)
        self.sp04_Label = Label(self.frame_4, text=u' ', height="1",width="5")
        self.sp04_Label.pack(side=LEFT, expand=YES)
        self.quitButton = Button(self.frame_4, text='Quit', command=self.quit)
        self.quitButton.pack(side=LEFT)
        self.frame_4.pack(side=TOP)

        self.frame_5 = Frame(master)
        self.sp05_Label = Label(self.frame_5, text=u' ', height="1",width="80")
        self.sp05_Label.pack(side=LEFT, expand=YES)
        self.frame_5.pack(side=TOP)
