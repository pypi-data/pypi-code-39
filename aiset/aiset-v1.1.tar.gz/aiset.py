#!/usr/bin/python
# -*- coding: UTF-8 -*-

# @Time    : 2019/07/02 10:04
# @Author  : xushaohui
# @FileName: aiset.py
# @Contact : xushaohui@wavewisdom-bj.com
# @Site    ：http://www.wavewisdom.com/index

from ftplib import FTP
import os
import sys
import time
import socket

class AISET_:   
    def __init__(self, host, port=827):               
        self.host = host
        self.port = port
        self.ftp = FTP()        
        self.ftp.encoding = 'gbk'
        self.file_list = []

    def login(self, username, password):        
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            self.ftp.set_pasv(True)
            self.ftp.connect(self.host, self.port)
            self.ftp.login(username, password)          
        except Exception as err:
            raise Exception('Connect Erro, you may input a wrong secret ...')           

    def is_same_size(self, local_file, remote_file):
        try:
            self.ftp.voidcmd('TYPE I')
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:            
            raise Exception('DataName Erro ...')            
        if os.path.exists(local_file):
            try:
                local_file_size = os.path.getsize(local_file)
            except Exception as err:                
                local_file_size = -1
        else:
            local_file_size = 2        
        if remote_file_size == local_file_size:
            return 1
        else:
            return 0

    def search_file(self,start_dir,files):
        self.ftp.cwd(start_dir)
        dir_res = []
        self.ftp.dir('.', dir_res.append)   
        for i in dir_res:
            if i.startswith("d"):                
                self.search_file(self.ftp.pwd()+"/"+i.split(" ")[-1],files)
                self.ftp.cwd('..')
            else:
                val = i.split(" ")[-1]               
                if self.ftp.pwd().endswith('/'): 
                    files.append(self.ftp.pwd()+'/'+val)             
                    pass
                else:  
                    files.append(self.ftp.pwd()+'/'+val)            
                    pass
            
    def download_file(self, local_file, remote_file):        
        if self.is_same_size(local_file, remote_file):
            print('You have got the same file %s,will not download this file.'%local_file)            
            return
        else:
            try:                
                buf_size = 1024
                file_handler = open(local_file, 'wb')
                self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
                file_handler.close()
            except Exception as err:               
                print('%s download Erro,please confirm' % local_file)
                return
            
    def download_file_tree(self,data_name,local_path):     
        remote_files=[]
        self.search_file(data_name,remote_files) 
        if local_path.endswith('/'):
            local_path=local_path[:-1]
        if local_path.endswith('\\'):
            local_path=local_path[:-1]        
        for remote_file in remote_files:               
            local_path_=local_path+remote_file
            print(local_path_)
            local_dir,local_name=os.path.split(local_path_)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)          
            self.download_file(local_path_, remote_file)
        return True
    def close(self):              
        self.ftp.quit()
def download(data_name,secret,local_path='./',ip="193.168.1.129"):
    AISET_TRANS = AISET_(ip)
    AISET_TRANS.login(data_name, secret)
    AISET_TRANS.download_file_tree( data_name,local_path)  
    AISET_TRANS.close()

if __name__ == "__main__":
    download('test','test')