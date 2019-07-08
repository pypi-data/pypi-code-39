from __future__ import unicode_literals

if __name__ == "__main__":
    raise

from googleapiclient.discovery import build
from youtube import Search
from youtube import Playlist
from youtube import Video

__title__ = 'youtube'
__author__ = "Katistic"
__version__ = "0.0.32"

client_set = False
client = None

def unescape(text): ## FOUND AT https://www.w3.org/QA/2008/04/unescape-html-entities-python, ported to py3
   """Removes HTML or XML character references
      and entities from a text string.
      keep &amp;, &gt;, &lt; in the source code.
   from Fredrik Lundh
   http://effbot.org/zone/re-sub.htm#unescape-html
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
            print("erreur de valeur")
            pass
      else:
         # named entity
         try:
            if text[1:-1] == "amp":
               text = "&amp;amp;"
            elif text[1:-1] == "gt":
               text = "&amp;gt;"
            elif text[1:-1] == "lt":
               text = "&amp;lt;"
            else:
               print(text[1:-1])
               text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
         except KeyError:
            print("keyerror")
            pass
      return text # leave as is
   return re.sub("&#?\w+;", fixup, text)

def setup(data):
    global client_set
    global client

    try:
        client = build(data["API_Service_Name"], data["API_Version"], developerKey = data["DevKey"])
    except:
        raise Exception("Failed to build client:", sys.exc_info[0])

    client_set = True

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
