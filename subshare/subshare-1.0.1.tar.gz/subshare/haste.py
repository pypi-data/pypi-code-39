#!/usr/bin/env python
# _____  _              _       _____       _    _  _
#|   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
#|__   || ||     || . || || | ||__   || | || . || || ||     || -_|
#|_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#
import requests

def Post(content, url):
    # Opens secified file and reads to a variable (content)
    with open(content, 'r') as content_file:
        content = content_file.read()
    # posts content file to hastebin
    post = requests.post(f'{url}/documents', data=content.encode('utf-8'))
    return(url + '/' + post.json()['key'])