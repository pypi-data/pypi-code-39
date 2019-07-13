
# Standard names for AAC tag fields
TAG_FIELDS = {
    'album_artist':         ['aART'],
    'artist':               ['\xa9ART'],
    'composer':             ['\xa9wrt'],
    'conductor':            ['cond'],
    'description':          ['desc'],
    'disc_id':              ['disc'],
    'orchestra':            ['orch'],
    'performer':            ['ense'],
    'album':                ['\xa9alb'],
    'title':                ['\xa9nam'],
    'genre':                ['\xa9gen'],
    'comment':              ['\xa9cmt'],
    'lyrics':               ['\xa9lyr'],
    'note':                 ['note'],
    'location':             ['loca'],
    'year':                 ['\xa9day'],
    'bpm':                  ['tmpo'],
    'rating':               ['rati'],
    'mcn':                  ['mcn\x00'],
    'label':                ['labe'],
    'copyright':            ['cprt'],
    'license':              ['lice'],
    'podcast_url':          ['purl'],
    'podcast_episode_guid': ['egid'],
    'podcast_category':     ['catg'],
    'podcast_keywords':     ['keyw'],
    'sort_album_artist':    ['soaa'],
    'sort_artist':          ['soar'],
    'sort_composer':        ['soco'],
    'sort_performers':      ['sopr'],
    'sort_show':            ['sosn'],
    'sort_album':           ['soal'],
    'sort_title':           ['sonm'],
    # Additional fields
    'replaygain':           ['repl'],
    'musicbrainz_id':       ['musi'],
    # iTunes grouping flag
    'grouping': ['\xa9grp'],
    # Indicates the encoder command used to encode track
    'encoder': ['\xa9too', 'enco'],
    # Another way iTunes stores tool info
    'itunes_tool': ['----:com.apple.iTunes:tool'],
    # iTunes encoder and normalization data
    'itunes_encoder': ['----:com.apple.iTunes:cdec'],
    'itunes_normalization': ['----:com.apple.iTunes:iTunNORM'],
    # XML info for song
    'itunes_movi': ['----:com.apple.iTunes:iTunMOVI'],
    # NO idea what this is
    'itunes_smbp': ['----:com.apple.iTunes:iTunSMPB'],
    # iTunes store purchase details
    'purchase_date': ['purd'],
    'purchaser_email': ['apID'],
    # Tags for video shows
    'video_show': ['tvsh'],
    'video_episode': ['tven'],
    # XID is internal itunes metadata reference
    'xid': ['xid'],
    # iTunes boolean flags
    'compilation': ['cpil'],
    'gapless_album': ['pgap'],
    'podcast': ['pcst'],
}

INTERNAL_FIELDS = (
    'replaygain',
    'musicbrainz_id',
    'grouping',
    'encoder',
    'itunes_tool',
    'itunes_encoder',
    'itunes_normalization',
    'itunes_movi',
    'itunes_smbp',
    'purchase_date',
    'purchaser_email',
    'video_show',
    'video_episode',
    'xid',
    'compilation',
    'gapless_album',
    'podcast',
)

INTEGER_FIELDS = (
    'bpm',
    'track_number',
    'total_tracks',
    'disk_number',
    'total_disks',
)

FLOAT_FIELDS = ()

BOOLEAN_FIELDS = (
    'compilation',
    'gapless_album',
    'podcast',
)
