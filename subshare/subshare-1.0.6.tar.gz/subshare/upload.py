#!/usr/bin/env python
# _____  _              _       _____       _    _  _
#|   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
#|__   || ||     || . || || | ||__   || | || . || || ||     || -_|
#|_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|
import owncloud
import sys
import os

def File(file, username, password, url, dir):
    nc = owncloud.Client(url)
    nc.login(username, password)
    fileName = os.path.basename(file)
    uploadDir = dir
    try:
        nc.put_file(uploadDir + "/" + fileName, file)
        link_info = nc.share_file_with_link(uploadDir + "/" + fileName)
        return(link_info.get_link())
    except:
        print("Please pass a path to a file")