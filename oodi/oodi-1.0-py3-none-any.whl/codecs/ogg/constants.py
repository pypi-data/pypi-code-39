
ALBUM_ART = 'METADATA_BLOCK_PICTURE'

TAG_FIELDS = {
    'album_artist':         ['ALBUM_ARTIST'],
    'artist':               ['ARTIST'],
    'arranger':             ['ARRANGER'],
    'author':               ['AUTHOR'],
    'composer':             ['COMPOSER'],
    'conductor':            ['CONDUCTOR'],
    'ensemble':             ['ENSEMBLE'],
    'orchestra':            ['ORCHESTRA'],
    'performer':            ['PERFORMER'],
    'publisher':            ['PUBLISHER'],
    'lyricist':             ['LYRICIST'],
    'album':                ['ALBUM'],
    'opus':                 ['OPUS'],
    'part':                 ['PART'],
    'title':                ['TITLE'],
    'part_number':          ['PARTNUMBER'],
    'genre':                ['GENRE'],
    'comment':              ['COMMENT'],
    'note':                 ['NOTE'],
    'description':          ['DESCRIPTION'],
    'location':             ['LOCATION'],
    'date':                 ['DATE'],
    'bpm':                  ['BPM'],
    'rating':               ['RATING'],
    'label':                ['LABEL'],
    'labelno':              ['LABELNO'],
    'isrc':                 ['ISRC'],
    'ean':                  ['EAN/UPN'],
    'lyrics':               ['LYRICS'],
    'website':              ['WEBSITE'],
    'copyright':            ['COPYRIGHT'],
    'license':              ['LICENSE'],
    'version':              ['VERSION'],
    'sourcemedia':          ['SOURCEMEDIA'],
    'encoding':             ['ENCODING'],
    'encoded_by':           ['ENCODED-BY'],
    'sort_album_artist':    ['SORT_ALBUM_ARTIST'],
    'sort_artist':          ['SORT_ARTIST'],
    'sort_composer':        ['SORT_COMPOSER'],
    'sort_performer':       ['SORT_PERFORMER'],
    'sort_show':            ['SORT_SHOW'],
    'sort_album':           ['SORT_ALBUM'],
    'sort_title':           ['SORT_TITLE'],
    'track_number':         ['TRACKNUMBER'],
    'total_tracks':         ['TRACKNUMBER'],
    'disk_number':          ['DISKNUMBER'],
    'total_disks':          ['DISKNUMBER'],
    'album_art':            ['METADATA_BLOCK_PICTURE'],
}

LIST_FIELDS = (
    'arranger',
    'author',
    'comment',
    'composer',
    'conductor',
    'performer',
    'date',
    'ensemble',
    'genre',
    'location',
    'lyricist',
    'part',
    'part_number',
    'performer',
)

INTERNAL_FIELDS = {
    'album_gain':           ['REPLAYGAIN_ALBUM_GAIN'],
    'album_peak':           ['REPLAYGAIN_ALBUM_PEAK'],
    'track_gain':           ['REPLAYGAIN_TRACK_GAIN'],
    'track_peak':           ['REPLAYGAIN_TRACK_PEAK'],
}

INTEGER_FIELDS = (
    'track_number',
    'total_tracks',
    'disk_number',
    'total_disks',
)

FLOAT_FIELDS = (
    'bpm',
)

BOOLEAN_FIELDS = ()
