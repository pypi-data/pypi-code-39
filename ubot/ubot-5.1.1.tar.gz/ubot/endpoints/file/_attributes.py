def _get_length(data_dict):
    track = data_dict.get('Video')
    if track is None:
        return

    width = track.get('Width')
    height = track.get('Height')
    if width < height:
        return width
    else:
        return height


attributes = {
    'audio': [
        ('duration', 'General', 'Duration'),
        ('performer', 'General', 'Performer'),
        ('title', 'General', 'Track')
    ],
    'video': [
        ('duration', 'General', 'Duration'),
        ('width', 'Video', 'Width'),
        ('height', 'Video', 'Height')
    ],
    'animation': [
        ('duration', 'General', 'Duration'),
        ('width', 'Video', 'Width'),
        ('height', 'Video', 'Height')
    ],
    'voice': [
        ('duration', 'General', 'Duration')
    ],
    'video_note': [
        ('duration', 'General', 'Duration'),
        ('length', _get_length, None),
    ]
}
