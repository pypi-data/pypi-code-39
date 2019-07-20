from __future__ import unicode_literals

if __name__ == "__main__":
    raise

#from youtube.Video import Video
import youtube

class Playlist:
    OtherProps = {}

    def __init__(self, data):
        data["class"] = "playlist"

        if type(data["id"]) == str:
            self.id = data["id"]
            self.kind = data["kind"].split("#")[1]
        else:
            self.id = data["id"]["playlistId"]
            self.kind = data["id"]["kind"].split("#")[1]

        s = data["snippet"]

        self.publishedAt = s["publishedAt"]
        self.channelId = s["channelId"]
        self.title = youtube.unescape(s["title"])
        self.description = youtube.unescape(s["description"])

        self.thumbnails = s["thumbnails"]
        self.channelTitle = s["channelTitle"]
        self.liveBroadcastContent = s["liveBroadcastContent"]

        self.OriginalData = data

class PlaylistItem:
    def __init__(self, data):
        data["class"] = "playlistItem"

        s = data["snippet"]
        self.id = s["resourceId"]["videoId"]
        self.kind = s["resourceId"]["kind"].split("#")[1]

        self.publishedAt = s["publishedAt"]
        self.channelId = s["channelId"]
        self.title = youtube.unescape(s["title"])
        self.description = youtube.unescape(s["description"])

        if "thumbnails" in s:
            self.thumbnails = s["thumbnails"]
        else:
            self.thumbnails = None
        self.channelTitle = s["channelTitle"]

        if self.title == "Private video" and self.description == "This video is private.":
            self.private = True
        else:
            self.private = False

        self.OriginalData = data

def _GetPlaylistItems(client, kwargs):
    if "ignore_private" in kwargs and type(kwargs["ignore_private"]) == bool:
        ignore_private = kwargs.pop("ignore_private")
    else:
        ignore_private = True

    response = client.playlistItems().list(**kwargs).execute()

    items = []
    for item in response["items"]:
        i = PlaylistItem(item)
        if ignore_private:
            if i.private == True:
                continue
        items.append(i)

    try:
        nextPageToken = response["nextPageToken"]
    except:
        nextPageToken = None

    #items.append(Video({'stuff': {"title": "break", "description": ""}}))

    while nextPageToken != None:
        response = client.playlistItems().list(**kwargs, pageToken=nextPageToken).execute()

        for item in response["items"]:
            for item in response["items"]:
                i = PlaylistItem(item)
                if ignore_private:
                    if i.private == True:
                        continue
                items.append(i)

        try:
            nextPageToken = response["nextPageToken"]
        except:
            nextPageToken = None

    return items

def GetPlaylistItems(client, playlist, ignore_private=True):
    id = playlist.playlistId

    kwargs = {
        'part': 'snippet',
        'maxResults': 50,
        'playlistId': id,
        'ignore+private': ignore_private
    }

    items = _GetPlaylistItems(client, kwargs)
    return items

def _GetFromId(client, kwargs):
    response = client.playlists().list(**kwargs).execute()

    if len(response['items']) < 0:
        raise Exception("Invalid playlist ID.")

    return Playlist(response["items"][0])

def GetFromId(client, id):
    kwargs = {
        'part': 'snippet',
        'id': id
    }

    return _GetFromId(client, kwargs)

def GetPlaylistItemsFromId(client, id):
    kwargs = {
        'part': 'snippet',
        'maxResults': 50,
        'playlistId': id
    }

    items = _GetPlaylistItems(client, kwargs)
    return items
