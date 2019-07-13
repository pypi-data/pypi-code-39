
def parse_exported_playlist_data(filename):
    """
    Example how to load playlist information text file exported
    from iTunes (applies to iOS device backups as well).

    This can be used to figure out which songs there were on a iOS device
    playlist, which the silly thing can't do itself. What you need to do
    is to:
    - connect the iOS device
    - select playlist from the iOS device
    - use File -> Library -> Export Playlist to export playlist info to text file
    - repeat for every playlist on iOS

    To import the playlist directly back to iTunes, just use 'Import Playlist' from
    menu and import the text file ... silly buggers!

    When you have the .txt files, you can use this function to reconstruct the
    playlist contents, to for example export the information to a normal .m3u
    playlist of tracks in your library.
    """
    from csv import reader
    tracks = []
    with open(filename, 'r', encoding='utf-16') as fd:
        rows = reader(fd, delimiter='\t')
        fields = next(rows)
        for row in rows:
            track = {}
            for i, field in enumerate(fields):
                track[field] = row[i]
            tracks.append(track)
    return tracks
