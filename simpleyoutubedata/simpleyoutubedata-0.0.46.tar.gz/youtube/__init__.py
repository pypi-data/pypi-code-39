from __future__ import unicode_literals

if __name__ == "__main__":
    raise

from googleapiclient.discovery import build
from youtube import HtmlEntityDefs as htmlentitydefs
from youtube import Search
from youtube import Playlist
from youtube import Video

import re
import sys

__title__ = 'youtube'
__author__ = "Katistic"
__version__ = "0.0.46"

client_set = False
client = None
online = False

setuprun = False
data = None

def IsOnline():
    return online

def unescape(text): ## FOUND AT https://www.w3.org/QA/2008/04/unescape-html-entities-python, ported to py3
   """Removes HTML or XML character references
      and entities from a text string.
   from Fredrik Lundh
   http://effbot.org/zone/re-sub.htm#unescape-html

   Ported to py3 by me
   """
   def fixup(m):
      text = m.group(0)
      if text[:2] == "&#":
         # character reference
         try:
            if text[:3] == "&#x":
               return chr(int(text[3:-1], 16))
            else:
               return chr(int(text[2:-1]))
         except ValueError:
            print("Value Error")
            pass
      else:
         # named entity
         try:
            #if text[1:-1] == "amp":
            #   text = "&amp;amp;"
            #elif text[1:-1] == "gt":
            #   text = "&amp;gt;"
            #elif text[1:-1] == "lt":
            #   text = "&amp;lt;"
            #else:
               #print(text[1:-1])
            text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
         except KeyError:
            print("Key Error")
            pass
      return text # leave as is
   return re.sub("&#?\w+;", fixup, text)

def setup(Data=None):
    global client_set
    global client
    global setuprun
    global data
    global online

    if not setuprun:
        data = Data
        setuprun = True
    else:
        Data = data

    try:
        client = build(Data["API_Service_Name"], Data["API_Version"], developerKey = Data["DevKey"])
        online = True
        client_set = True
    except:
        print("Failed to build client:", sys.exc_info())
        #raise Exception("Failed to build client:", sys.exc_info[0])

def ClientNotSetErr():
    raise Exception("Client has not been set.")

def SetClient(devkey):
    data = {
        "DevKey": devkey,
        "API_Service_Name": "youtube",
        "API_Version": "v3"
    }

    setup(data)

def _valid_client():
    if client != None:
        return True
    elif setuprun:
        setup()
        if client != None:
            return True

    return False

def _setup():
    if client_set and _valid_client:
        return True
    return False

class search:
    def videos(**kwargs):
        if client_set:
            data = Search.Videos(client, kwargs)
            return data
        else:
            ClientNotSetErr()

    def playlists(**kwargs):
        if client_set:
            data = Search.Playlists(client, kwargs)
            return data
        else:
            ClientNotSetErr()

    def channels(**kwargs):
        if client_set:
            data = Search.Channels(client, kwargs)
            return data
        else:
            ClientNotSetErr()

class playlist:
    def getItems(playlistObj):
        if client_set:
            data = Playlist.GetPlaylistItems(client, playlistObj)
            return data
        else:
            ClientNotSetErr()

    def getItemsFromId(id):
        if client_set:
            return Playlist.GetPlaylistItemsFromId(client, id)
        else:
            ClientNotSetErr()

    def getFromId(id):
        if client_set:
            return Playlist.GetFromId(client, id)
        else:
            ClientNotSetErr()

class video:
    def getFromId(id):
        if client_set:
            return Video.GetFromId(client, id)
        else:
            ClientNotSetErr()
