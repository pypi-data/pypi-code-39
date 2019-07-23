from soco import SoCo
import dateutil.parser
import time
import sys

class SonosExtras(SoCo):
    
    def stop_after(self):
        self.print_current_status()
        current_track = self.get_current_track_info()
        position = dateutil.parser.parse(current_track['position'])
        duration = dateutil.parser.parse(current_track['duration'])
        remainingSeconds = (duration - position).seconds
        while remainingSeconds > 0:
            try:
                print("\rWainting for the song to end in " + remainingSeconds.__str__(), end = '    ', flush=True)
                remainingSeconds -= 1
                time.sleep(1)
            except KeyboardInterrupt:
                print("\nCancelled by user!")
                return 1
        print()
        self.pause()
        
    def playlists(self):
        allLists = self.my_zone.get_sonos_playlists()
        for ourList in allLists:
            print(ourList.item_id + " | " + ourList.title)
        print("Total: " + allLists.number_returned.__str__())
    
    def playlist(self, title):
        try:
            ourList = self.my_zone.get_sonos_playlist_by_attr('title', title)
        except ValueError:
            try:
                ourList = self.my_zone.get_sonos_playlist_by_attr('item_id', title)
            except ValueError:
                print("No playlist matched " + title)
                return

        print("playlist " + title + " exists")

    def print_queue(self):
        count = 0
        queue = self.my_zone.get_queue()
        print("Total " + queue.total_matches.__str__() + " items in queue:")
        returned_matches = queue.number_returned
        while queue.total_matches >= returned_matches and queue.number_returned > 0 :
            for item in queue:
                try:
                    count = count + 1
                    item_dict = item.__dict__
                    item_dict["artist"] = count.__str__() + " | " + item_dict["creator"]
                    item_dict["uri"] = item_dict["resources"][0].__str__()
                    if not 'album' in item_dict.keys(): item_dict["album"] = "N/A"
                    # print(item_dict)
                    self.print_track(item_dict)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
            queue = self.my_zone.get_queue(returned_matches)
            returned_matches = returned_matches + queue.number_returned
        
    def print_current_status(self):
        print(self.get_current_transport_info())
        current_track = self.get_current_track_info()
        print(current_track['position'], ' / ', current_track['duration'])
        self.print_track(current_track)

    def print_track(self, track):
        line = ''
        if track["playlist_position"]  != '': line = track["playlist_position"] + " | "
        if track["artist"]  != '': line = line + track["artist"] + " | "
        if track["album"]   != '': line = line + track["album"] + " | "
        if track["title"]   != '': line = line + track["title"] + " | "
        if track["uri"]   != '': line = line + track["uri"]
        print(line)
