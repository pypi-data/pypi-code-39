from __future__ import unicode_literals

if __name__ == "__main__":
    raise

#from youtube.Video import Video
import youtube

class Playlist:
    OtherProps = {}

    def __init__(self, data):
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
        self.id = data["contentDetails"]["videoId"].split("#")[1]

        s = data["snippet"]
        self.kind = s["resourceId"]["kind"]

        self.publishedAt = s["publishedAt"]
        self.channelId = s["channelId"]
        self.title = youtube.unescape(s["title"])
        self.description = youtube.unescape(s["description"])

        self.thumbnails = s["thumbnails"]
        self.channelTitle = s["channelTitle"]

def _GetPlaylistItems(client, kwargs):
    response = client.playlistItems().list(**kwargs).execute()

    items = []
    for item in response["items"]:
        items.append(Video(item))

    try:
        nextPageToken = response["nextPageToken"]
    except:
        nextPageToken = None

    #items.append(Video({'stuff': {"title": "break", "description": ""}}))

    while nextPageToken != None:
        response = client.playlistItems().list(**kwargs, pageToken=nextPageToken).execute()

        for item in response["items"]:
            items.append(PlaylistItem(item))

        try:
            nextPageToken = response["nextPageToken"]
        except:
            nextPageToken = None

    return items

def GetPlaylistItems(client, playlist):
    id = playlist.playlistId

    kwargs = {
        'part': 'snippet',
        'maxResults': 50,
        'playlistId': id
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
