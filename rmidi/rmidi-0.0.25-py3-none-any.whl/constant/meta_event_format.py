# X = {
#     "0xFF": {
#         "id": 255,
#         "name": "meta",
#         "0x00": {
#             "type_id": 0,
#             "type_name": "sequence_number",
#             "length": 2,
#             "params": [
#                 "nmsb",
#                 "nlsb"
#             ],
#             "dtype": "int",
#             "mask": [
#                 255,
#                 255
#             ],
#             "default" : [0, 0]
#         },
#         "0x01": {
#             "type_id": 1,
#             "type_name": "text_event",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "Enter the Text"
#         },
#         "0x02": {
#             "type_id": 2,
#             "type_name": "copyright_notice",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "No Copyright"
#         },
#         "0x03": {
#             "type_id": 3,
#             "type_name": "track_name",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "Track 0"
#         },
#         "0x04": {
#             "type_id": 4,
#             "type_name": "instrument_name",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "Piano"
#         },
#         "0x05": {
#             "type_id": 5,
#             "type_name": "lyrics",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "LYRICS"
#         },
#         "0x06": {
#             "type_id": 6,
#             "type_name": "marker",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "*"
#         },
#         "0x07": {
#             "type_id": 7,
#             "type_name": "cue_point",
#             "length": -1,
#             "params": "text",
#             "dtype": "str",
#             "mask": 127,
#             "default" : "-"
#         },
#         "0x20": {
#             "type_id": 32,
#             "type_name": "midi_ch_prefix",
#             "length": 1,
#             "params": [
#                 "channel"
#             ],
#             "dtype": "int",
#             "mask": [
#                 15
#             ],
#             "default" : [0]
#         },
#         "0x21": {
#             "type_id": 33,
#             "type_name": "midi_port",
#             "length": 1,
#             "params": [
#                 "port_no"
#             ],
#             "dtype": "int",
#             "mask": [
#                 15
#             ],
#             "default" : [0]
#         },
#         "0x2F": {
#             "type_id": 47,
#             "type_name": "end_of_track",
#             "length": 0,
#             "params": None,
#             "dtype": "None",
#             "mask": 127,
#             "default" : None
#         },
#         "0x51": {
#             "type_id": 81,
#             "type_name": "set_tempo",
#             "length": 3,
#             "params": [
#                 "musec_per_quat_note",
#                 "musec_per_quat_note",
#                 "musec_per_quat_note"
#             ],
#             "dtype": "int",
#             "mask": [
#                 127,
#                 127,
#                 127
#             ],
#             "default" : [0, 0, 0]
#         },
#         "0x54": {
#             "type_id": 84,
#             "type_name": "smpte_offset",
#             "length": 5,
#             "params": [
#                 "hr",
#                 "min",
#                 "sec",
#                 "fr",
#                 "subfr"
#             ],
#             "dtype": "int",
#             "mask": [
#                 24,
#                 60,
#                 60,
#                 30,
#                 100
#             ],
#             "default" : [0, 0 , 0, 0, 0]
#         },
#         "0x58": {
#             "type_id": 88,
#             "type_name": "time_sig",
#             "length": 4,
#             "params": [
#                 "numer",
#                 "denom",
#                 "metro",
#                 "32nds"
#             ],
#             "dtype": "int",
#             "mask": [
#                 255,
#                 255,
#                 255,
#                 255
#             ],
#             "default" : [0, 0, 0, 0]
#         },
#         "0x59": {
#             "type_id": 89,
#             "type_name": "key_sig",
#             "length": 2,
#             "params": [
#                 "key",
#                 "scale"
#             ],
#             "dtype": "int",
#             "mask": [
#                 15,
#                 1
#             ],
#             "default" : [0, 1]
#         },
#         "0x7F": {
#             "type_id": 127,
#             "type_name": "sequence_specifier",
#             "length": -1,
#             "params": "text",
#             "dtype": "any",
#             "mask": 127,
#             "default" : [0]
#         }
#     }
# }

X = {
        255: {
            0: {'dtype': 'int',
                'length': 2,
                'mask': (255, 255),
                'params': ('nmsb', 'nlsb'),
                'type_id': 0,
                'type_name': 'sequence_number'},
            1: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 1,
                'type_name': 'text_event'},
            2: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 2,
                'type_name': 'copyright_notice'},
            3: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 3,
                'type_name': 'track_name'},
            4: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 4,
                'type_name': 'instrument_name'},
            5: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 5,
                'type_name': 'lyrics'},
            6: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 6,
                'type_name': 'marker'},
            7: {'dtype': 'str',
                'length': -1,
                'mask': 127,
                'params': 'text',
                'type_id': 7,
                'type_name': 'cue_point'},
            32: {'dtype': 'int',
                    'length': 1,
                    'mask': (15,),
                    'params': ('channel',),
                    'type_id': 32,
                    'type_name': 'midi_ch_prefix'},
            33: {'dtype': 'int',
                    'length': 1,
                    'mask': (15,),
                    'params': ('port_no',),
                    'type_id': 33,
                    'type_name': 'midi_port'},
            47: {'dtype': 'None',
                    'length': 0,
                    'mask': 127,
                    'params': None,
                    'type_id': 47,
                    'type_name': 'end_of_track'},
            81: {'dtype': 'int',
                    'length': 3,
                    'mask': (127, 127, 127),
                    'params': ('musec_per_quat_note',
                            'musec_per_quat_note',
                            'musec_per_quat_note'),
                    'type_id': 81,
                    'type_name': 'set_tempo'},
            84: {'dtype': 'int',
                    'length': 5,
                    'mask': (24, 60, 60, 30, 100),
                    'params': ('hr', 'min', 'sec', 'fr', 'subfr'),
                    'type_id': 84,
                    'type_name': 'smpte_offset'},
            88: {'dtype': 'int',
                    'length': 4,
                    'mask': (255, 255, 255, 255),
                    'type_id': 88,
                    'type_name': 'time_sig'},
            89: {'dtype': 'int',
                    'length': 2,
                    'mask': (15, 1),
                    'params': ('key', 'scale'),
                    'type_id': 89,
                    'type_name': 'key_sig'},
            127: {'dtype': 'any',
                    'length': -1,
                    'mask': 127,
                    'params': 'text',
                    'type_id': 127,
                    'type_name': 'sequence_specifier'},
            'id': 255,
            'name': 'meta'
            }
        }